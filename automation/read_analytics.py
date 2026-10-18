"""Read aggregate Cloudflare analytics. Credentials are environment-only.
No report is published, logged or committed automatically.
"""
import datetime as dt,json,os,re,sys,urllib.request,urllib.error
from zoneinfo import ZoneInfo
UTC=dt.timezone.utc
QUERY='''query Traffic($zoneTag: string, $filter: filter) { viewer { zones(filter: {zoneTag: $zoneTag}) { httpRequestsAdaptiveGroups(limit: 1000, filter: $filter, orderBy: [datetimeHour_ASC]) { count sum { visits edgeResponseBytes } dimensions { datetimeHour } } } } }'''
def period(day,now=None):
 now=now or dt.datetime.now(UTC);local=ZoneInfo('Europe/Rome')
 start=dt.datetime.combine(dt.date.fromisoformat(day),dt.time(),local)
 end=min(start+dt.timedelta(days=1),now.astimezone(local))
 if end<=start:raise ValueError('Date is in the future')
 return start.astimezone(UTC),end.astimezone(UTC)
def summarize(data,start,end):
 if data.get('errors'):raise ValueError('Cloudflare query rejected; check token permissions and dataset availability')
 zones=(data.get('data') or {}).get('viewer',{}).get('zones')
 if not zones or len(zones)!=1:raise ValueError('Requested zone not available')
 rows=zones[0].get('httpRequestsAdaptiveGroups')
 if rows is None:raise ValueError('Analytics dataset unavailable')
 if not rows:return {'status':'no_data','start':start.isoformat(),'end':end.isoformat(),'requests':None,'cloudflare_visits':None}
 for row in rows:
  if row.get('count') is None or row.get('sum',{}).get('visits') is None:raise ValueError('Incomplete analytics response')
 return {'status':'ok','start':start.isoformat(),'end':end.isoformat(),'timezone':'Europe/Rome','requests':sum(r['count'] for r in rows),'cloudflare_visits':sum(r['sum']['visits'] for r in rows),'bytes':sum(r['sum'].get('edgeResponseBytes',0) for r in rows),'note':'Cloudflare adaptive dataset: counts may be estimated; visits are Cloudflare’s metric, not verified unique people. Bots and internal tests are not independently excluded. No merchant-click or sales metrics included.'}
def read(day):
 token=os.environ.get('CLOUDFLARE_ANALYTICS_TOKEN','');zone=os.environ.get('CLOUDFLARE_ZONE_ID','')
 if not token or not re.fullmatch('[a-fA-F0-9]{32}',zone):raise ValueError('Missing analytics token or invalid zone ID')
 start,end=period(day)
 body={'query':QUERY,'variables':{'zoneTag':zone,'filter':{'datetime_geq':start.isoformat(),'datetime_lt':end.isoformat(),'clientRequestHTTPHost':'offerte4zampe.it','requestSource':'eyeball'}}}
 req=urllib.request.Request('https://api.cloudflare.com/client/v4/graphql',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+token,'Content-Type':'application/json','Accept':'application/json'})
 try:
  with urllib.request.urlopen(req,timeout=30) as response:data=json.load(response)
 except (urllib.error.URLError,TimeoutError):raise ValueError('Cloudflare API unavailable; no report generated') from None
 return summarize(data,start,end)
if __name__=='__main__':
 try:
  day=sys.argv[1] if len(sys.argv)>1 else dt.datetime.now(ZoneInfo('Europe/Rome')).date().isoformat()
  result=read(day)
  # Explicit local output only. Do not run with public CI logs.
  print(json.dumps(result,ensure_ascii=False,indent=2))
 except (ValueError,KeyError,TypeError):
  print('Analytics unavailable: check date, token, zone and API dataset permissions. No zero totals inferred.',file=sys.stderr);sys.exit(1)
