import copy
import datetime as dt
import html
import json
import unittest
from automation.audit_store_integrity import verify_page, apply_evidence, fingerprint, select, report
from automation.package_integrity import reconcile


class StoreIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.now=dt.datetime(2026,10,28,15,tzinfo=dt.timezone.utc)
        self.offer=dict(id='bauzaar:1',merchant_id='bauzaar',merchant='Bauzaar',title='Patè 85 gr - confezione da 24 pezzi',variant='1ct',price=24,available=True,gtin='4006381333931',weight_kg=2.04,brand='Brand',url='https://www.bauzaar.it/products/food?variant=1')

    def shopify(self,**changes):
        v=dict(id=1,title='Patè',price=100,available=True,barcode='4006381333931');v.update(changes)
        return json.dumps({'variants':[v]})

    def test_selling_multipack_compared_against_unit_page_price_without_false_alarm(self):
        r=verify_page(self.offer,self.shopify())
        self.assertEqual(r['status'],'verified');self.assertEqual(r['discrepancies'],[])
        self.assertEqual(r['evidence']['pack_count'],24);self.assertEqual(r['evidence']['price'],24)
        self.assertEqual(r['evidence']['net_weight_kg'],2.04)
        self.assertEqual(verify_page(self.offer,self.shopify(id=2))['status'],'inconclusive')

    def test_real_price_and_stock_difference_are_detected(self):
        r=verify_page(self.offer,self.shopify(price=200,available=False))
        self.assertEqual(set(r['discrepancies']),{'price','available'})
        entry=dict(r,source='https://www.bauzaar.it/products/food.js',checked_at=self.now.isoformat(),fingerprint=fingerprint(self.offer))
        original=copy.deepcopy(self.offer);apply_evidence([self.offer],{self.offer['id']:entry},self.now)
        self.assertEqual(self.offer,original)

    def test_feed_net_weight_conflict_requires_fresh_exact_page_evidence(self):
        o=dict(self.offer,title='Lettiera 5 lt (4 kg)',variant='4,4kg',weight_kg=4.4)
        reconcile(o);self.assertIsNone(o['weight_kg']);self.assertTrue(o['weight_conflict'])
        r=verify_page(o,self.shopify(title='5 lt (4 kg)',price=2400))
        entry=dict(r,source='https://www.bauzaar.it/products/food.js',checked_at=self.now.isoformat(),fingerprint=fingerprint(o))
        self.assertEqual(apply_evidence([o],{o['id']:entry},self.now)[0]['fields'],['weight_kg'])
        self.assertEqual(o['weight_kg'],4);self.assertNotIn('weight_conflict',o)
        stale=dict(o,weight_kg=None);self.assertEqual(apply_evidence([stale],{o['id']:entry},self.now+dt.timedelta(days=8)),[])

    def test_isola_schema_must_identify_exact_sku(self):
        o=dict(self.offer,id='isola-dei-tesori:001',merchant_id='isola-dei-tesori',title='Food',price=5,weight_kg=None)
        p={'@type':'Product','sku':'001','offers':{'priceCurrency':'EUR','price':'5.00','availability':'https://schema.org/InStock'}}
        body=lambda:'<script type="application/ld+json">'+json.dumps(p)+'</script>'
        self.assertEqual(verify_page(o,body())['discrepancies'],[])
        p['sku']='002';self.assertEqual(verify_page(o,body())['status'],'inconclusive')

    def test_paco_schema_barcode_cannot_override_different_selected_variant(self):
        o=dict(self.offer,id='paco:1',merchant_id='paco',title='Food',feed_gtin='4006381333931',price=5,quantity_verified=False)
        p={'@type':'Product','sku':'1','gtin13':'4006381333931','offers':{'priceCurrency':'EUR','price':'5.00','availability':'https://schema.org/InStock'}}
        selected={'id':'1','price_amount':5,'attributes':{'1':{'name':'2 kg','ean13':'9780201379624'}}}
        body=lambda:'<script type="application/ld+json">'+json.dumps(p)+'</script><div data-product="'+html.escape(json.dumps(selected),quote=True)+'">'
        self.assertEqual(verify_page(o,body())['reason'],'selected_pack_not_bound_to_feed_barcode')
        selected['attributes']['1']['ean13']='4006381333931'
        r=verify_page(o,body());self.assertEqual(r['status'],'verified');self.assertEqual(r['evidence']['net_weight_kg'],2)

    def test_all_stores_have_a_budget_and_rotation_does_not_repeat_recent_checks(self):
        origins={'bauzaar':'https://www.bauzaar.it/products/food?variant=1','webpet':'https://www.webpet.it/products/food?variant=1','animaliapet':'https://www.animaliapet.eu/products/food?variant=1','isola-dei-tesori':'https://www.isoladeitesori.it/prodotto/food/1.html','paco':'https://www.pacopetshop.it/it/brand/1-food.htm'}
        offers=[dict(self.offer,id=s+':1',merchant_id=s,url=u) for s,u in origins.items()]
        chosen=select(offers,{},self.now,1);self.assertTrue(all(len(rows)==1 for rows in chosen.values()))
        cache={o['id']:{'fingerprint':fingerprint(o),'checked_at':self.now.isoformat(),'source':o['url'],'status':'inconclusive','reason':'network','discrepancies':[],'compared':[]} for o in offers}
        self.assertTrue(all(not rows for rows in select(offers,cache,self.now,1).values()))
        result=report({'offers':offers,'generated_at':self.now.isoformat()},cache,self.now)
        self.assertTrue(all(s['sample_verified']==0 and s['sample_inconclusive']==1 for s in result['stores']))

    def test_page_evidence_invalidated_by_changed_native_code_or_variant(self):
        original=fingerprint(self.offer)
        self.assertNotEqual(original,fingerprint(dict(self.offer,feed_gtin='9780201379624')))
        self.assertNotEqual(original,fingerprint(dict(self.offer,variant='12 kg')))
        self.assertEqual(original,fingerprint(dict(self.offer,feed_gtin=self.offer['gtin'].zfill(14))))
