import datetime as dt
import unittest
from automation.build_product_catalog import build,clean_title,quantity

class CanonicalProductTests(unittest.TestCase):
    def setUp(self):
        self.now=dt.datetime(2026,10,28,12,tzinfo=dt.timezone.utc)
        self.a=dict(id='a:1',merchant_id='a',merchant='A',title='Acana - Acana Adult 2 kg',variant='2 kg',brand='Acana',price=20,available=True,gtin='4006381333931',weight_kg=2,checked_at=self.now.isoformat(),url='https://shop.test/a')
    def model(self,rows,old=None):return build({'offers':rows,'generated_at':self.now.isoformat()},old,now=self.now)
    def test_gtin_and_selling_quantity_define_product_not_price_or_shop(self):
        b=dict(self.a,id='b:1',merchant_id='b',merchant='B',price=18,gtin='04006381333931')
        m=self.model([self.a,b]);self.assertEqual(len(m['products']),1);self.assertEqual(m['metrics']['multi_shop_products'],1)
        p=m['products'][0];self.assertEqual(p['active_shop_count'],2);self.assertEqual(p['name'],'Acana Adult 2 kg')
        self.assertEqual({o['product_id'] for o in m['offers']},{p['id']})
        b['price']=17;b['title']='Acana Adult Cane 2 kg'
        second=self.model([self.a,b],m['registry']);self.assertEqual(second['products'][0]['slug'],p['slug'])
    def test_single_store_multiple_offers_is_not_a_multishop_comparison(self):
        m=self.model([self.a,dict(self.a,id='a:2')]);self.assertEqual(m['metrics']['multi_shop_products'],0)
        self.assertEqual(m['products'][0]['verified_shop_count'],1)
    def test_missing_gtin_and_different_formats_are_never_fuzzy_merged(self):
        rows=[self.a,dict(self.a,id='b:1',merchant_id='b',gtin=''),dict(self.a,id='c:1',merchant_id='c',weight_kg=4)]
        self.assertEqual(len(self.model(rows)['products']),3)
    def test_unknown_merchant_quantity_never_acquires_unit_price(self):
        row=dict(self.a,quantity_verified=False);m=self.model([row]);self.assertIsNone(m['offers'][0]['unit_price'])
        self.assertEqual(m['products'][0]['matching_method'],'unattached')
    def test_titles_and_explicit_volume_pieces(self):
        self.assertEqual(clean_title('Mousse 85 g 85 gr - Cibo umido per gatti'),'Mousse 85 g')
        self.assertEqual(quantity(dict(title='Lettiera 6 x 5 l'))['volume_ml'],30000)
        self.assertEqual(quantity(dict(title='Snack 12 pezzi'))['pieces'],12)
        self.assertIsNone(quantity(dict(title='Lettiera 5 l / 10 l'))['volume_ml'])
    def test_stale_and_sold_out_do_not_inflate_metric(self):
        b=dict(self.a,id='b:1',merchant_id='b',available=False)
        self.assertEqual(self.model([self.a,b])['products'][0]['active_shop_count'],1)

    def test_capacity_is_not_misrepresented_as_consumable_volume(self):
        self.assertIsNone(quantity(dict(title='Ciotola in acciaio 500 ml'))['volume_ml'])
        self.assertIsNone(quantity(dict(title='Acquario 100 l'))['volume_ml'])
        self.assertEqual(quantity(dict(title='Shampoo per cani 250 ml'))['volume_ml'],250)
        self.assertEqual(quantity(dict(title='Lettiera 36 L (6 confezioni da 6 litri)'))['volume_ml'],36000)

    def test_observed_history_and_retired_products_keep_identity(self):
        catalog={'offers':[self.a],'generated_at':self.now.isoformat()}
        history={'offers':{'a:1':[{'day':'2026-10-27','low':19,'high':21,'last':20,'available':True}]}}
        first=build(catalog,history=history,now=self.now)
        self.assertEqual(first['products'][0]['history'][0]['sum'],20)
        retired=build({'offers':[],'generated_at':self.now.isoformat()},first['registry'],now=self.now)
        self.assertEqual(retired['products'][0]['id'],first['products'][0]['id'])
        self.assertEqual(retired['products'][0]['active_offer_count'],0)

    def test_explicit_brand_line_aliases_need_same_gtin_and_quantity(self):
        a=dict(self.a,brand='Royal Canin Veterinary Diet')
        b=dict(self.a,id='b:1',merchant_id='b',brand='Royal Canin')
        self.assertEqual(self.model([a,b])['metrics']['multi_shop_products'],1)
        for extra in [{'brand':'Unrelated Royal Canin imitation'},{'weight_kg':4},{'gtin':''}]:
            self.assertEqual(self.model([a,dict(b,**extra)])['metrics']['multi_shop_products'],0)
        # Corporate ownership alone is not an alias.
        self.assertEqual(self.model([dict(a,brand='Askoll'),dict(b,brand='Ciano')])['metrics']['multi_shop_products'],0)

    def test_brand_merge_preserves_existing_urls_with_unambiguous_redirect(self):
        from unittest.mock import patch
        a=dict(self.a,brand='Royal Canin Veterinary Diet')
        b=dict(self.a,id='b:1',merchant_id='b',brand='Royal Canin')
        with patch('automation.build_product_catalog.BRAND_ALIASES',{}):old=self.model([a,b])
        new=self.model([a,b],old['registry'])
        current=next(p for p in new['products'] if p['active_offer_count'])
        retired=next(p for p in new['products'] if not p['active_offer_count'])
        self.assertEqual(retired['redirect_slug'],current['slug'])
        self.assertEqual(current['slug'],next(p['slug'] for p in old['products'] if p['brand']=='Royal Canin'))
        missing=self.model([b],old['registry'])
        self.assertNotIn('redirect_slug',next(p for p in missing['products'] if not p['active_offer_count']))
        self.assertEqual(new['metrics']['store_coverage']['b']['offers_in_multishop_products'],1)
