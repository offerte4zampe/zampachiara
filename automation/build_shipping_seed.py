"""Convert current JSON rules to versioned rows without implementing shipping maths.

Fail on unmapped fields/overlapping intervals. SQL is generated for staging only;
regenerating it never executes a database migration.
"""
import argparse
import datetime as dt
from decimal import Decimal
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIELDS={'name','fee','free_from','free_above','boundary_unknown','max_shipping_weight_kg','source','note','checked_at','verified_until'}

def stamp(value):
    parsed=dt.datetime.fromisoformat(value.replace('Z','+00:00'))
    if parsed.tzinfo is None:parsed=parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')

def integer(value,multiplier):
    n=Decimal(str(value))*multiplier
    if not n.is_finite() or n<0 or n!=n.to_integral_value():raise ValueError('Non-integral or invalid base amount: '+str(value))
    return int(n)

def validate_intervals(rows):
    buckets={}
    for row in rows:
        start=stamp(row['valid_from']);end=stamp(row['valid_to']) if row.get('valid_to') else None
        if end and end<=start:raise ValueError('Invalid interval')
        buckets.setdefault((row['shop_id'],row['zone']),[]).append((start,end))
    for key,intervals in buckets.items():
        previous=None
        for start,end in sorted(intervals):
            if previous and (previous[1] is None or start<previous[1]):raise ValueError('Overlapping rules: '+str(key))
            previous=(start,end)

def convert(payload):
    rows=[];shops=[]
    for sid,r in sorted(payload['merchants'].items()):
        extra=set(r)-FIELDS-{'conflict'}
        if extra:raise ValueError('Unmapped shipping fields for '+sid+': '+str(sorted(extra)))
        checked=stamp(r.get('checked_at') or payload['checked_at'])
        # The legacy source used seven days in trade.js. JSON now explicitly owns it.
        until=r.get('verified_until')
        if not until:
            days=payload.get('verification_max_age_days')
            if not isinstance(days,(int,float)) or isinstance(days,bool) or days<=0:raise ValueError('Explicit verification expiry is required')
            until=(dt.datetime.fromisoformat(checked.replace('Z','+00:00'))+dt.timedelta(days=days)).isoformat()
        until=stamp(until)
        if until<checked:raise ValueError('Verification ends before its observation')
        if 'free_from' in r and 'free_above' in r:raise ValueError('Conflicting threshold modes')
        threshold=r.get('free_from',r.get('free_above'))
        boundary=r.get('boundary_unknown')
        if boundary is not None and (threshold is None or integer(boundary,100)!=integer(threshold,100)):raise ValueError('Unmapped boundary exception')
        conflict=r.get('conflict',False)
        status='uncertain' if conflict else 'verified' if 'fee' in r else 'unknown'
        shops.append(dict(id=sid,name=r.get('name') or sid))
        rows.append(dict(shop_id=sid,zone='IT',std_cents=integer(r['fee'],100) if status=='verified' else None,
            free_from_cents=integer(threshold,100) if status=='verified' and threshold is not None else None,
            threshold_mode='unknown' if boundary is not None or threshold is None else 'inclusive' if 'free_from' in r else 'exclusive',
            max_weight_g=integer(r['max_shipping_weight_kg'],1000) if r.get('max_shipping_weight_kg') is not None else None,
            over_weight_note=r.get('note'),status=status,source_url=r.get('source'),notes='\n'.join(x for x in (payload.get('scope'),r.get('note')) if x),
            verified_at=checked,verified_until=until,valid_from=checked,valid_to=None))
    validate_intervals(rows)
    return dict(shops=shops,rules=rows)

def literal(value):
    if value is None:return 'NULL'
    if isinstance(value,int):return str(value)
    return "'"+str(value).replace("'","''")+"'"

def sql_seed(data):
    out=['-- Generated from site/data/shipping-rules.json; staging only.','-- Expired observations remain expired; generation does not reverify sources.','BEGIN TRANSACTION;']
    for table,records in [('shop',data['shops']),('shipping_rule',data['rules'])]:
        for row in records:
            keys=list(row)
            conflict='id' if table=='shop' else 'shop_id,zone,valid_from'
            # UPSERT preserves rule PKs; never use REPLACE, which deletes rows.
            update=','.join(k+'=excluded.'+k for k in keys if k not in ('id','shop_id','zone','valid_from'))
            out.append('INSERT INTO '+table+' ('+','.join(keys)+') VALUES ('+','.join(literal(row[k]) for k in keys)+') ON CONFLICT('+conflict+') DO UPDATE SET '+update+';')
    return '\n'.join(out+['COMMIT;',''])

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,default=ROOT/'site/data/shipping-rules.json');parser.add_argument('--output',type=Path,default=ROOT/'worker/seeds/shipping-rules.sql');parser.add_argument('--json',action='store_true');args=parser.parse_args()
    data=convert(json.loads(args.source.read_text()))
    if args.json:print(json.dumps(data,ensure_ascii=False));return
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(sql_seed(data));print('Staging seed:',args.output,len(data['rules']),'rules')
if __name__=='__main__':main()
