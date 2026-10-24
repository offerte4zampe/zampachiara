"""Import public merchant catalogs; use approved official feeds where available; never invent prices."""
import gzip
import concurrent.futures, datetime, json, os, re, time, urllib.request, urllib.robotparser
from decimal import Decimal, InvalidOperation
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCES=[('bauzaar','Bauzaar','https://www.bauzaar.it'),('webpet','WebPet','https://www.webpet.it'),('animaliapet','Animaliapet','https://www.animaliapet.eu'),('isola-dei-tesori','Isola dei Tesori','https://www.isoladeitesori.it'),('paco','Paco Pet Shop','https://www.pacopetshop.it')]
UA='Offerte a 4 ZampeCatalog/1.0 (+https://offerte4zampe.it/contatti.html)'
def get(url):
    req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'application/json,text/plain'})
    with urllib.request.urlopen(req,timeout=35) as r:
        if r.status!=200: raise ValueError('HTTP '+str(r.status))
        return r.read()
def amount(v):
    try:
        d=Decimal(str(v)); return float(d) if d.is_finite() and 0<d<100000 else None
    except (InvalidOperation,ValueError): return None
def weight(label):
    # Only explicitly labelled package weights. Shipping grams are NOT net weight.
    s=label.lower().replace(',','.')
    s=re.sub(r'(?<=\d)\s*gr\b|\bgr\b', 'g', s)
    # A life-stage suffix is not a bonus quantity (e.g. Adult 5+ 15 kg).
    s=re.sub(r'\b(adult|senior|ageing|mature|maxi|medium|mini)\s+\d{1,2}\s*\+', r'\1', s)
    if '+' in s: return None
    if re.search(r'\d\s*[-–/]\s*\d|\b(?:peso del cane|peso corporeo|cani da|fino a|oltre)\b',s): return None
    if re.search(r'\d+\s*(?:pz|pezzi|lattine|buste|bustine|confezioni)\b',s) and not re.search(r'\d+\s*[x×]',s): return None
    pack=re.search(r'(\d+)\s*[x×]\s*(\d+(?:\.\d+)?)\s*(kg|g)\b',s)
    if pack: return round(int(pack[1])*float(pack[2])/(1000 if pack[3]=='g' else 1),6)
    matches=list(re.finditer(r'(?<![\d.])(\d+(?:\.\d+)?)\s*(kg|g)\b',s))
    if len(matches)==1:return float(matches[0][1])/(1000 if matches[0][2]=='g' else 1)
    return None
def collect(source, shipping_only=False):
    sid,name,base=source; now=datetime.datetime.now(datetime.timezone.utc).isoformat(); rows=[]
    try:
        if sid=='paco':
            from paco_feed import collect as paco_collect
            return paco_collect()
        if sid=='isola-dei-tesori':
            from isola_feed import collect as isola_collect
            return isola_collect()
        if sid=='bauzaar' and not shipping_only:
            from bauzaar_feed import collect as official_collect
            from shipping_metadata import supplement
            rows,status=official_collect()
            supplement(rows,lambda:collect(source,True),ROOT/'automation/shipping-cache.json')
            return rows,status
        rp=urllib.robotparser.RobotFileParser();rp.parse(get(base+'/robots.txt').decode().splitlines())
        if not rp.can_fetch(UA,base+'/products.json'):raise ValueError('Catalog access disallowed by robots')
        seen=set(); complete=False
        for page in range(1,101):
            products=json.loads(get(f'{base}/products.json?limit=250&page={page}'))['products']
            if not products:complete=True;break
            for p in products:
                if str(p['id']) in seen: raise ValueError('Repeated pagination')
                seen.add(str(p['id']))
                for v in p.get('variants',[]):
                    price=amount(v.get('price'))
                    if not price:continue
                    variant=v.get('title',''); variant='' if variant=='Default Title' else variant
                    title=str(p['title']);kg=weight(variant) if re.search(r'\d\s*(?:kg|g)\b',variant.lower()) else weight(title)
                    before=amount(v.get('compare_at_price'))
                    rows.append({'id':f'{sid}:{v["id"]}','merchant':name,'merchant_id':sid,'title':title,'variant':variant,'brand':p.get('vendor',''),'category':p.get('product_type',''),'price':price,'previous_price':before if before and before>price else None,'available':bool(v.get('available')),'url':base+'/products/'+p['handle']+'?variant='+str(v['id']),'image':(p.get('images') or [{}])[0].get('src',''),'sku':str(v.get('sku') or ''),'gtin':str(v.get('barcode') or ''),'weight_kg':kg,'shipping_weight_kg':(amount(v.get('grams'))/1000 if amount(v.get('grams')) else None),'checked_at':now})
            if len(products)<250:complete=True;break
            time.sleep(.3)
        if not complete:raise ValueError('Catalog exceeded pagination safety limit')
        return rows,{'id':sid,'name':name,'status':'ok','checked_at':now,'offers':len(rows),'source':base+'/products.json','method':'Catalogo pubblico del negozio'}
    except Exception as e:
        return [],{'id':sid,'name':name,'status':'error','checked_at':now,'offers':0,'error':type(e).__name__,'source':base+'/products.json'}
def main():
    path=ROOT/'site/data/catalog.json';old=json.loads(gzip.decompress(path.with_suffix('.json.gz').read_bytes())) if path.with_suffix('.json.gz').exists() else {'offers':[]}
    offers=[];sources=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for rows,status in pool.map(collect,SOURCES):
            if status['status']=='error':
                rows=[r for r in old.get('offers',[]) if r['merchant_id']==status['id']];status['offers']=len(rows);status['status']='stale' if rows else 'error'
            offers.extend(rows);sources.append(status)
    # Preserve official partner snapshots; stale dates remain visible to the UI.
    public_ids={s[0] for s in SOURCES}
    for partner in old.get('sources',[]):
        if partner['id'] not in public_ids and partner.get('method')=='Feed ufficiale normalizzato':
            rows=[r for r in old['offers'] if r['merchant_id']==partner['id']]
            offers.extend(rows);sources.append(partner)
    payload={'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'refresh_hours':6,'tracking_enabled':any(o.get('affiliate_url') for o in offers),'sources':sources,'offers':offers}
    if not offers: raise SystemExit('No verified offers available; previous catalog unchanged')
    path.parent.mkdir(exist_ok=True);tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')));tmp.replace(path)
    path.with_suffix('.json.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
    print(json.dumps({'offers':len(offers),'sources':sources},ensure_ascii=False))
if __name__=='__main__':main()
