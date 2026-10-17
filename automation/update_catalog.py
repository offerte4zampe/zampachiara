"""Import public merchant catalogs; never generate affiliate links or invented prices."""
import gzip
import concurrent.futures, datetime, json, os, re, time, urllib.request, urllib.robotparser
from decimal import Decimal, InvalidOperation
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCES=[('bauzaar','Bauzaar','https://www.bauzaar.it'),('webpet','WebPet','https://www.webpet.it'),('animaliapet','Animaliapet','https://www.animaliapet.eu')]
UA='Offerte4ZampeCatalog/1.0 (+https://offerte4zampe.it/contatti.html)'
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
    if '+' in s: return None
    if re.search(r'\d+\s*(?:pz|pezzi|lattine|buste|bustine|confezioni)\b',s) and not re.search(r'\d+\s*[x×]',s): return None
    pack=re.search(r'(\d+)\s*[x×]\s*(\d+(?:\.\d+)?)\s*(kg|g)\b',s)
    if pack: return round(int(pack[1])*float(pack[2])/(1000 if pack[3]=='g' else 1),6)
    matches=list(re.finditer(r'(?<![\d.])(\d+(?:\.\d+)?)\s*(kg|g)\b',s))
    if len(matches)==1:return float(matches[0][1])/(1000 if matches[0][2]=='g' else 1)
    return None
def collect(source):
    sid,name,base=source; now=datetime.datetime.now(datetime.timezone.utc).isoformat(); rows=[]
    try:
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
                    rows.append({'id':f'{sid}:{v["id"]}','merchant':name,'merchant_id':sid,'title':title,'variant':variant,'brand':p.get('vendor',''),'category':p.get('product_type',''),'price':price,'previous_price':before if before and before>price else None,'available':bool(v.get('available')),'url':base+'/products/'+p['handle']+'?variant='+str(v['id']),'image':(p.get('images') or [{}])[0].get('src',''),'sku':str(v.get('sku') or ''),'gtin':str(v.get('barcode') or ''),'weight_kg':kg,'checked_at':now})
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
    payload={'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'refresh_hours':6,'tracking_enabled':False,'sources':sources,'offers':offers}
    if not offers: raise SystemExit('No verified offers available; previous catalog unchanged')
    path.parent.mkdir(exist_ok=True);tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')));tmp.replace(path)
    path.with_suffix('.json.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
    print(json.dumps({'offers':len(offers),'sources':sources},ensure_ascii=False))
if __name__=='__main__':main()
