import unittest
from automation.brand_landings import brand_pages
from automation.apply_brand_links import apply
class BrandLandingTests(unittest.TestCase):
    def test_threshold_exact_names_and_preserved_legacy_slugs(self):
        offers=[{'brand':name} for name,count in [('Royal Canin',5),('royal-canin',5),('Élite & Cane',6),('Small',4)] for _ in range(count)]
        pages=dict((name,slug) for slug,name in brand_pages(offers))
        self.assertEqual(pages['Royal Canin'],'royal-canin')
        self.assertNotEqual(pages['royal-canin'],'royal-canin')
        self.assertEqual(pages['Élite & Cane'],'elite-cane')
        self.assertNotIn('Small',pages)
        self.assertEqual(len(set(pages.values())),len(pages))
    def test_internal_brand_queries_and_home_are_canonical_and_idempotent(self):
        html='<main><div id="home-brands"><a href="confronta-cibo.html?brand=Marca">Marca</a></div><a href="https://shop.test/?brand=Marca">Negozio</a></main>'
        pages={'Marca':'/marca-marca'}
        out=apply(html,pages)
        self.assertIn('href="/marca-marca"',out)
        self.assertIn('https://shop.test/?brand=Marca',out)
        self.assertIn('home-all-brands',out)
        self.assertEqual(out,apply(out,pages))
