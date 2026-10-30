import unittest
from automation.build_priority_products import select
from automation.enrich_catalog import lookup_priority

class PriorityProductTests(unittest.TestCase):
    def model(self):
        p=dict(id='p1',name='Line',brand='Brand',slug='line',active_shop_count=2,
               verified_shop_count=2,quantity={'verified':True,'kind':'mass'},
               species='cane',category='crocchette',format='2 kg',gtin='4006381333931',offer_ids=['a','b'])
        offers=[dict(id=i,merchant_id=shop,available=True,gtin='4006381333931') for i,shop in [('a','a'),('b','b')]]
        offers.append(dict(id='c',merchant_id='c',available=True,gtin='',feed_gtin='4006381333931',quantity_verified=False))
        return dict(generated_at='2026-10-30',products=[p],offers=offers)
    def test_feed_lead_is_not_counted_as_verified_shop(self):
        r=select(self.model());p=r['products'][0]
        self.assertEqual(p['verified_shops'],2);self.assertEqual(p['missing_shops'],1)
        self.assertEqual(p['candidate_offer_ids'],['c']);self.assertEqual(r['at_target'],0)
        self.assertIn('c',r['priority_offer_ids'])
    def test_sold_out_or_same_store_is_not_third_store_lead(self):
        for change in [{'available':False},{'merchant_id':'a'}]:
            m=self.model();m['offers'][-1].update(change)
            self.assertEqual(select(m)['with_third_store_lead'],0)
    def test_cap_determinism_and_ineligible_products(self):
        m=self.model();m['products'] += [dict(m['products'][0],id='p2')]
        self.assertEqual(select(m,brand_cap=1)['selected'],1)
        m['products'][0]['quantity']={'verified':False,'kind':'mass'}
        self.assertEqual(select(m)['selected'],1)
    def test_priority_does_not_override_missing_barcode_first(self):
        self.assertLess(lookup_priority([{'id':'x'}],.1,{'x'}),lookup_priority([{'id':'y'}],1,{'x'}))
        self.assertLess(lookup_priority([{'id':'y'}],.1,{'x'}),lookup_priority([{'id':'x','gtin':'4006381333931'}],1,{'x'}))
