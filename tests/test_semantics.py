import unittest
from automation.apply_semantics import apply
class SemanticTests(unittest.TestCase):
    def test_empty_headings_removed_and_levels_do_not_skip(self):
        html='<h1>Page</h1><h3>Section</h3><h5></h5><h4>Detail</h4>'
        self.assertEqual(apply(html),'<h1>Page</h1><h2>Section</h2><h3>Detail</h3>')
        self.assertEqual(apply(apply(html)),apply(html))
    def test_product_card_name_is_subordinate(self):
        out=apply('<h1>Page</h1><h2>Offers</h2><article class="catalog-card"><h2>Food</h2></article>')
        self.assertIn('<h3>Food</h3>',out)
