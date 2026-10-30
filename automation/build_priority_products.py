"""Operational shortlist, not a popularity ranking or matching authorization."""
import gzip,json
from collections import Counter,defaultdict
from pathlib import Path
try:
    from .audit_store_integrity import canonical_gtin
except ImportError:
    from audit_store_integrity import canonical_gtin
ROOT=Path(__file__).resolve().parents[1]


def select(model,limit=300,brand_cap=15):
    offers={o['id']:o for o in model['offers']}
    by_code=defaultdict(list)
    for o in model['offers']:
        code=canonical_gtin(o.get('feed_gtin') or o.get('gtin'))
        if code and o.get('available') is True:by_code[code].append(o)
    eligible=[]
    for p in model['products']:
        if not p['active_shop_count'] or not p['quantity']['verified']:continue
        if p['species'] not in ('cane','gatto','cane e gatto'):continue
        if p['category'] not in ('crocchette','umido','snack','lettiere'):continue
        if p['quantity']['kind']=='sales_unit':continue
        rows=[offers[i] for i in p['offer_ids'] if i in offers]
        shops={o['merchant_id'] for o in rows if o.get('available') is True}
        candidates=[o for o in by_code.get(canonical_gtin(p.get('gtin')),[]) if o['merchant_id'] not in shops]
        # Feed codes alone do not prove whole-pack equivalence or availability freshness.
        pending=sorted({o['id'] for o in candidates})
        count=p['verified_shop_count']
        row={'product_id':p['id'],'name':p['name'],'brand':p['brand'],
             'category':p['category'],'species':p['species'],'format':p['format'],
             'url':'https://offerte4zampe.it/prodotto/'+p['slug'],
             'verified_shops':count,'target_shops':3,'missing_shops':max(0,3-count),
             'offer_ids':p['offer_ids'],'candidate_offer_ids':pending,
             'next_action':'maintain_coverage' if count>=3 else 'verify_feed_package' if pending else 'find_additional_store',
             'candidate_warning':'Shared feed GTIN is a lead only; package, variant, price and freshness must be verified.'}
        # Two-store products with an existing third-store lead are the first recovery work.
        rank=(0 if count==2 and pending else 1 if count>=3 else 2 if count==2 else 3 if pending else 4,p['brand'].casefold(),p['id'])
        eligible.append((rank,row))
    selected=[];brands=Counter()
    for _,row in sorted(eligible):
        if brands[row['brand'].casefold()]>=brand_cap:continue
        selected.append(row);brands[row['brand'].casefold()]+=1
        if len(selected)>=limit:break
    priority_ids=sorted({oid for p in selected if p['missing_shops'] for oid in p['offer_ids']+p['candidate_offer_ids']})
    return {'generated_at':model['generated_at'],'selection_basis':'Operational opportunity and category/brand diversity; no search-demand data used.',
            'target':limit,'selected':len(selected),'brand_cap':brand_cap,
            'at_target':sum(p['verified_shops']>=3 for p in selected),
            'with_third_store_lead':sum(p['verified_shops']==2 and bool(p['candidate_offer_ids']) for p in selected),
            'categories':dict(Counter(p['category'] for p in selected)),
            'priority_offer_ids':priority_ids,'products':selected}


def main():
    model=json.loads(gzip.decompress((ROOT/'site/data/product-catalog.json.gz').read_bytes()))
    report=select(model)
    (ROOT/'site/data/priority-products.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('products','priority_offer_ids')},ensure_ascii=False))

if __name__=='__main__':main()
