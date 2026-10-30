import unittest
from automation.route_product_links import apply


class ProductRoutingTests(unittest.TestCase):
    def test_titles_and_buttons_internal_but_merchant_choice_preserves_tracking(self):
        offers = [{'id':'a:1','product_slug':'cibo-2kg','title':'Cibo','url':'https://shop.test/a','affiliate_url':'https://tc.tradetracker.net/?c=1&a=2'}]
        title = '<a class="product-title-link" href="https://tc.tradetracker.net/?c=1&amp;a=2" rel="sponsored" target="_blank">Cibo</a>'
        button = '<a href="https://shop.test/a" rel="sponsored">Vai al negozio ↗</a>'
        out = apply(title+button, offers)
        self.assertEqual(out.count('/prodotto/cibo-2kg'),2)
        self.assertNotIn('sponsored',out)
        self.assertIn('Confronta nei negozi',out)
        self.assertEqual(apply(out,offers),out)
        detail = apply(title+button,offers,merchant_choice=True)
        self.assertIn('/go/a%3A1?from=product',detail)
        self.assertIn('sponsored nofollow noopener noreferrer',detail)
        self.assertIn('class="product-title-link" href="/prodotto/',detail)

    def test_ambiguous_formats_not_guessed_and_unknown_urls_unchanged(self):
        offers = [{'id':'a','title':'A','url':'https://shop.test/same'}, {'id':'b','product_slug':'cibo-b','title':'B','url':'https://shop.test/same'}]
        self.assertNotIn('href=',apply('<a href="https://shop.test/same">Formato incerto</a>',offers))
        self.assertIn('/prodotto/cibo-b',apply('<a href="https://shop.test/same">B</a>',offers))
        unknown='<a href="https://shop.test/shipping">Spedizione</a>'
        self.assertEqual(apply(unknown,offers),unknown)
