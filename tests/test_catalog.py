import unittest, importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('catalog',Path(__file__).parents[1]/'automation/update_catalog.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class CatalogTests(unittest.TestCase):
 def test_pack_weights(self):
  for label,kg in [('12 kg',12),('800 g',.8),('Patè 85 gr Agnello - confezione da 24 pezzi',2.04),('Mousse 85 g 85 gr - confezione da 24 pezzi',2.04),('Camon Snacks Box 500 gr Duo stars',.5),('12 x 85 g',1.02),('2 × 12 kg',24),('Formato: 1,5 kg',1.5),('Royal Canin Maxi 5+ Senior 15 kg',15),('Mousse 85gr',.085),('Adult 5+ 12 kg',12),('30 pz x 1 gr',.03),('1 gr x 30',.03),('7 pz x 1 gr',.007),('2gx30pz',.06),('30 compresse da 0,5 gr',.015),('24 lattine da 400 g',9.6)]:
   self.assertAlmostEqual(m.weight(label),kg)
 def test_no_shipping_or_ambiguous_weight(self):
  for label in ['Default Title','85 g 100 g - confezione da 24 pezzi','2 x 85 g - confezione da 24 pezzi','1 g x 2.5','21.5 x 5.7 cm','1 kg / 3 kg','Misure: 20 cm','12 + 2 kg','6 pezzi 85 g','15 kg+3 kg Omaggio','cani da 10-25 kg','Adult 12 kg / 15 kg','Adult 12+2 kg','Adult 12 + 2 kg']:
   self.assertIsNone(m.weight(label))
 def test_no_fake_or_invalid_price(self):
  for value in ['NaN','Infinity',0,-1,None,'gratis']:
   self.assertIsNone(m.amount(value))
  self.assertEqual(m.amount('12.49'),12.49)
if __name__=='__main__':unittest.main()
