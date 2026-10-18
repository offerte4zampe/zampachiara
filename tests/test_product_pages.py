import importlib.util, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('products',Path(__file__).resolve().parents[1]/'automation/build_product_pages.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
class ProductIdentity(unittest.TestCase):
 def test_different_recipe_or_shop_never_merged(self):
  a=dict(merchant='A',title='Adult pollo',brand='B')
  self.assertFalse(mod.same_product(a,dict(a,title='Adult salmone')))
  self.assertFalse(mod.same_product(a,dict(a,merchant='C')))
  self.assertTrue(mod.same_product(a,dict(a,variant='12 kg')))
