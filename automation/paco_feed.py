"""Approved Paco TradeTracker catalog. Never infer selling quantity from a unit GTIN."""
import concurrent.futures
import datetime as dt
import html
import json
import re
import urllib.request
import urllib.robotparser
from urllib.parse import urlsplit, parse_qs
from bauzaar_feed import amount, value

FEED_URL='https://pf.tradetracker.net/?aid=518044&encoding=utf-8&type=json&fid=1216771&categoryType=2&additionalType=2'
ORIGIN='https://www.pacopetshop.it'
UA='Offerte4Zampe/1.0 (+https://offerte4zampe.it/contatti.html)'

def normalize(payload, now=None):
    now=now or dt.datetime.now(dt.timezone.utc)
    rows=[];seen=set()
    for p in payload['products']:
        ident=str(p.get('ID',''))
        if p.get('campaignID')!=24833 or not ident.isdigit() or ident in seen: raise ValueError('Unexpected campaign or duplicate ID')
        seen.add(ident)
        link=p['URL'];u=urlsplit(link);q=parse_qs(u.query)
        if u.scheme!='https' or u.netloc!='www.pacopetshop.it' or u.path!='/directlinking/' or q.get('tt')!=['24833_1216771_518044_'] or len(q.get('r',[]))!=1: raise ValueError('Unexpected tracking URL')
        dest=q['r'][0];target=urlsplit(dest)
        if target.scheme!='https' or target.netloc!='www.pacopetshop.it' or not re.fullmatch(r'/it/[^/]+/'+re.escape(ident)+r'-[^/]+\.htm',target.path) or target.query or target.fragment: raise ValueError('Exact product destination required')
        if p.get('variations'): raise ValueError('Unmapped variations')
        props=p.get('properties',{});stock=value(props,'availability')
        if stock not in ('in stock','out of stock','preorder','backorder'): raise ValueError('Unknown stock')
        price=p['price'];regular=amount(price.get('amount'))
        if price.get('currency')!='EUR': raise ValueError('Invalid currency')
        if regular is None: continue
        sale=value(props,'sale_price')
        if sale:
            m=re.fullmatch(r'(\d+(?:\.\d+)?) EUR',sale)
            if not m or amount(m[1]) is None: raise ValueError('Invalid current feed price')
            current=amount(m[1])
            if current>regular: raise ValueError('Inconsistent feed price')
        else: current=regular
        title=html.unescape(p['name']).strip()
        if not title: raise ValueError('Missing title')
        # A barcode in this feed may describe one unit of a merchant multipack.
        # Keep it as evidence, never as an automatic matching key without quantity proof.
        rows.append(dict(id='paco:'+ident,merchant='Paco Pet Shop',merchant_id='paco',title=title,
            variant='Formato e ricetta da verificare nel negozio',brand=html.unescape(value(props,'brand')),
            category=value(props,'product_type'),price=current,previous_price=None,available=stock=='in stock',
            url=dest,affiliate_url=link,image=(p.get('images') or [''])[0],sku=value(props,'MPN'),
            gtin='',feed_gtin=value(props,'GTIN'),weight_kg=None,shipping_weight_kg=None,
            checked_at=now.isoformat(),source_type='official_feed',quantity_verified=False))
    if not rows: raise ValueError('Empty feed')
    return rows

def verify_quantity(row, page):
    """Bind only the current selected variant whose code AND whole-pack price match."""
    from update_catalog import weight
    match=re.search(r'data-product="([^"]+)"',page)
    if not match: return row
    try:
        p=json.loads(html.unescape(match[1]));attrs=list(p.get('attributes',{}).values())
        codes={str(a.get('ean13','')).strip() for a in attrs if a.get('ean13')}
        if codes!={row['feed_gtin']} or not codes: return row
        if abs(float(p['price_amount'])-row['price'])>.005: return row
        labels=[str(a.get('name','')) for a in attrs]
        quantities=[x for x in labels if re.search(r'\d\s*(?:kg|gr|g)\b',x,re.I)]
        if len(quantities)!=1: return row
        kg=weight(re.sub(r'\bgr\b','g',quantities[0],flags=re.I))
        if not kg or not 0<kg<=1000: return row
        # The explicit label must account for all units; bare title weight is insufficient.
        return dict(row,variant=' · '.join(labels),gtin=row['feed_gtin'],weight_kg=kg,
                    weight_source='merchant:selected_variant',quantity_verified=True)
    except (ValueError,KeyError,TypeError): return row

def collect():
    now=dt.datetime.now(dt.timezone.utc)
    with urllib.request.urlopen(urllib.request.Request(FEED_URL,headers={'User-Agent':UA}),timeout=90) as response:
        raw=response.read(40000001);modified=response.headers.get('Last-Modified')
    if len(raw)>40000000: raise ValueError('Feed too large')
    rows=normalize(json.loads(raw),now)
    # Bounded read-only verification; all uncertain packages remain outside matching.
    from pathlib import Path
    import gzip
    catalog=Path(__file__).resolve().parents[1]/'site/data/catalog.json.gz'
    try: peers={str(o.get('gtin','')).lstrip('0') for o in json.loads(gzip.decompress(catalog.read_bytes()))['offers'] if o.get('weight_kg')}
    except (OSError,ValueError): peers=set()
    chosen=sorted(range(len(rows)),key=lambda i:(rows[i]['feed_gtin'].lstrip('0') not in peers,rows[i]['id']))[:40]
    rp=urllib.robotparser.RobotFileParser()
    try:
        with urllib.request.urlopen(urllib.request.Request(ORIGIN+'/robots.txt',headers={'User-Agent':UA}),timeout=15) as response: rp.parse(response.read().decode().splitlines())
        def inspect(i):
            row=rows[i]
            if not rp.can_fetch(UA,row['url']): return i,row
            try:
                with urllib.request.urlopen(urllib.request.Request(row['url'],headers={'User-Agent':UA}),timeout=12) as response: page=response.read(3000000).decode('utf-8')
                return i,verify_quantity(row,page)
            except Exception: return i,row
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            for i,row in pool.map(inspect,chosen): rows[i]=row
    except Exception: pass
    return rows,dict(id='paco',name='Paco Pet Shop',status='ok',offers=len(rows),checked_at=now.isoformat(),
        source='TradeTracker:1216771',method='Feed ufficiale TradeTracker · aggiornamento giornaliero',
        retrieved_at=now.isoformat(),upstream_last_modified=modified,
        verified_quantities=sum(r['quantity_verified'] for r in rows))
