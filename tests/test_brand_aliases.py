import unittest
from automation.brand_landings import brand_pages,in_scope,canonical_brand
from automation.build_brand_pages import money
class BrandAliasTests(unittest.TestCase):
    def test_alias_counts_share_one_landing_and_do_not_change_unknown_names(self):
        offers=[{'brand':b} for b in ['Aldog']*3+['AlDog']*3+['Farmina N&D Ocean']*3+['N&D Farmina']*3]
        pages={name:slug for slug,name in brand_pages(offers)}
        self.assertEqual(set(pages),{'AlDog','Farmina'})
        self.assertEqual(canonical_brand('LifeCat'),'Life Cat')
        self.assertEqual(canonical_brand('Monge BWild'),'Monge')
        self.assertEqual(canonical_brand('Independent Brand'),'Independent Brand')
    def test_fishing_tackle_is_outside_catalog_and_prices_use_italian_format(self):
        self.assertFalse(in_scope({'brand':'RAPALA'}))
        self.assertTrue(in_scope({'brand':'Tetra'}))
        self.assertEqual(money(1234.5),'1.234,50 €')
