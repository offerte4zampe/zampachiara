import unittest, importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('catalog',Path(__file__).parents[1]/'automation/update_catalog.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class CatalogTests(unittest.TestCase):
 def test_pack_weights(self):
  for label,kg in [('12 kg',12),('800 g',.8),('12 x 85 g',1.02),('2 × 12 kg',24),('Formato: 1,5 kg',1.5)]:
   self.assertAlmostEqual(m.weight(label),kg)
 def test_no_shipping_or_ambiguous_weight(self):
  for label in ['Default Title','21.5 x 5.7 cm','1 kg / 3 kg','Misure: 20 cm','12 + 2 kg','24 lattine da 400 g','6 pezzi 85 g']:
   self.assertIsNone(m.weight(label))
 def test_no_fake_or_invalid_price(self):
  for value in ['NaN','Infinity',0,-1,None,'gratis']:
   self.assertIsNone(m.amount(value))
  self.assertEqual(m.amount('12.49'),12.49)
if __name__=='__main__':unittest.main()
