"""Daily observed min/max prices; no backfill and no fabricated historical points."""
import gzip,json,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def update(history,catalog,today):
 cutoff=(datetime.date.fromisoformat(today)-datetime.timedelta(days=89)).isoformat()
 rows=history.get('offers',{})
 for oid in list(rows):
  rows[oid]=[r for r in rows[oid] if r['day']>=cutoff]
  if not rows[oid]:del rows[oid]
 for o in catalog['offers']:
  # Failed imports retain old data: never invent an observation for the current day.
  if o['checked_at'][:10]!=today:continue
  items=rows.setdefault(o['id'],[]);previous=next((r for r in items if r['day']==today),None)
  if previous:
   previous.update(low=min(previous['low'],o['price']),high=max(previous['high'],o['price']),last=o['price'],available=o['available'],checked_at=o['checked_at'])
  else:items.append({'day':today,'low':o['price'],'high':o['price'],'last':o['price'],'available':o['available'],'checked_at':o['checked_at']})
 return {'started_at':history.get('started_at',today),'updated_at':catalog['generated_at'],'retention_days':90,'offers':rows}
def build():
 p=ROOT/'site/data/price-history.json.gz';old=json.loads(gzip.decompress(p.read_bytes())) if p.exists() else {}
 catalog=json.loads(gzip.decompress((ROOT/'site/data/catalog.json.gz').read_bytes()));today=datetime.datetime.now(datetime.timezone.utc).date().isoformat()
 d=update(old,catalog,today);p.write_bytes(gzip.compress(json.dumps(d,separators=(',',':')).encode(),mtime=0));print('Observed history:',len(d['offers']),'offers since',d['started_at'])
if __name__=='__main__':build()
