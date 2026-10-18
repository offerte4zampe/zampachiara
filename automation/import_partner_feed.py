"""Validate a normalized official partner export before merging into the catalog.
Input is private/local: never commit raw exports or feed credentials.
"""
import datetime as dt
import gzip,json,math,sys
from pathlib import Path
from urllib.parse import urlsplit
MERCHANTS={'arcaplanet':('Arcaplanet','arcaplanet.it'),'isoladeitesori':("L’Isola dei Tesori",'isoladeitesori.it'),'zooplus':('zooplus','zooplus.it')}
def normalize(payload,now=None):
 now=now or dt.datetime.now(dt.timezone.utc)
 sid=payload['merchant_id'];name,domain=MERCHANTS[sid]
 stamp=dt.datetime.fromisoformat(payload['checked_at'].replace('Z','+00:00'))
 if stamp.tzinfo is None or not -300<=(now-stamp).total_seconds()<=36*3600:raise ValueError('Feed timestamp missing, future or stale')
 if payload.get('source_type')!='official_feed':raise ValueError('Official feed provenance required')
 rows=[];seen=set()
 for r in payload['offers']:
  key=str(r['id']);u=urlsplit(r['url']);price=r['price']
  if not key or key in seen:raise ValueError('Missing or duplicate offer ID')
  seen.add(key)
  if u.scheme!='https' or u.username or u.password or not (u.hostname==domain or (u.hostname or '').endswith('.'+domain)):raise ValueError('Unexpected merchant URL')
  if isinstance(price,bool) or not isinstance(price,(int,float)) or not math.isfinite(price) or price<=0:raise ValueError('Invalid price')
  if type(r['available']) is not bool:raise ValueError('Explicit stock status required')
  if not str(r['title']).strip():raise ValueError('Missing title')
  kg=r.get('weight_kg')
  if kg is not None and (isinstance(kg,bool) or not isinstance(kg,(int,float)) or not math.isfinite(kg) or kg<=0 or not r.get('weight_source')):raise ValueError('Explicit net weight provenance required')
  rows.append(dict(id=sid+':'+key,merchant=name,merchant_id=sid,title=r['title'],variant=r.get('variant',''),brand=r.get('brand',''),category=r.get('category',''),price=price,previous_price=None,available=r['available'],url=r['url'],image='',sku=r.get('sku',''),gtin=r.get('gtin',''),weight_kg=kg,shipping_weight_kg=None,checked_at=stamp.isoformat()))
 if not rows:raise ValueError('Empty feed: retain existing catalog')
 return rows,dict(id=sid,name=name,status='ok',offers=len(rows),checked_at=stamp.isoformat(),source='Feed ufficiale partner',method='Feed ufficiale normalizzato')
def merge(catalog,payload,now=None):
 rows,source=normalize(payload,now);sid=source['id']
 return dict(catalog,offers=[o for o in catalog['offers'] if o['merchant_id']!=sid]+rows,sources=[s for s in catalog.get('sources',[]) if s['id']!=sid]+[source])
if __name__=='__main__':
 path=Path(__file__).resolve().parents[1]/'site/data/catalog.json.gz'
 result=merge(json.loads(gzip.decompress(path.read_bytes())),json.loads(Path(sys.argv[1]).read_text()))
 tmp=path.with_suffix('.tmp');tmp.write_bytes(gzip.compress(json.dumps(result,ensure_ascii=False,separators=(',',':')).encode(),mtime=0));tmp.replace(path)
 print('Validated official feed imported; run enrichment and page builders before publishing.')
