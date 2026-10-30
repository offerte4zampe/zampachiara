import unittest
from automation.clean_urls import apply, clean_url, product_url


class CanonicalURLTests(unittest.TestCase):
    def test_paths_queries_fragments_and_affiliate_bytes(self):
        self.assertEqual(clean_url('index.html?x=1#main'), '/?x=1#main')
        self.assertEqual(clean_url('/offerte/index.html'), '/offerte/')
        self.assertEqual(clean_url('confronta-cibo.html?brand=A&amp;shop=B#results'), '/confronta-cibo?brand=A&shop=B#results')
        self.assertEqual(clean_url('/google123.html'), '/google123.html')
        source='<a href="https://tc.tradetracker.net/?a=1&amp;b=2">Shop</a>'
        self.assertEqual(apply(source), source)
        self.assertEqual(apply(apply(source)), source)

    def test_exact_id_to_slug_without_touching_commercial_destination(self):
        offer={'id':'a:1','product_slug':'brand-2kg','url':'https://shop.test/a?aff=1'}
        source='<a href="prodotto.html?id=a%3A1">Cibo</a>'
        self.assertEqual(apply(source, {'a:1':offer}), '<a href="/prodotto/brand-2kg">Cibo</a>')
        self.assertEqual(offer['url'],'https://shop.test/a?aff=1')
        self.assertEqual(clean_url('prodotto.html?id=unknown', {'a:1':offer}), 'prodotto.html?id=unknown')
        self.assertEqual(product_url({'product_slug':'//evil.test'}), '/confronta-cibo')

    def test_old_gtin_page_points_directly_to_canonical_product(self):
        self.assertEqual(clean_url('prezzi-old.html',redirects={'/prezzi-old':'/prodotto/exact-2kg'}), '/prodotto/exact-2kg')
