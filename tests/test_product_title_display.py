import unittest
from automation.build_product_catalog import clean_title
from automation.apply_product_metadata import apply
class ProductTitleDisplayTests(unittest.TestCase):
    def test_spacing_and_separators_do_not_repeat_selling_format(self):
        for name in ['Cibo 15 kg · 15kg','Cibo 15 kg 15 kg','Cibo 15kg']:
            self.assertEqual(clean_title(name,variant='15kg').replace('15 kg','15kg'),'Cibo 15kg')
        self.assertEqual(clean_title('Cibo 2 kg / 4 kg'),'Cibo 2 kg / 4 kg')
    def test_formatter_is_loaded_once_before_legacy_client(self):
        html='<script src="assets/product.js?v=1" defer></script>'
        out=apply(html);self.assertEqual(out,apply(out));self.assertLess(out.index('product-metadata.js'),out.index('product.js'))
