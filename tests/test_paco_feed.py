import unittest,sys,json,html,copy
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'automation'))
from paco_feed import normalize,verify_quantity
def fixture():
 return {'products':[{'ID':'123','campaignID':24833,'name':'Test cibo','price':{'currency':'EUR','amount':24},'URL':'https://www.pacopetshop.it/directlinking/?tt=24833_1216771_518044_&r=https%3A%2F%2Fwww.pacopetshop.it%2Fit%2Fbrand%2F123-test.htm','properties':{'availability':['out of stock'],'sale_price':['20.00 EUR'],'GTIN':['4006381333931'],'brand':['Brand']},'variations':[]}]}
class PacoFeedTest(unittest.TestCase):
 def test_feed_stock_tracking_price_without_unit_inference(self):
  r=normalize(fixture())[0];self.assertEqual(r['price'],20);self.assertFalse(r['available']);self.assertEqual(r['gtin'],'');self.assertIsNone(r['weight_kg']);self.assertIn('tt=24833_',r['affiliate_url']);self.assertIsNone(r['previous_price'])
 def test_verified_multipack_and_mismatch(self):
  r=normalize(fixture())[0];p={'price_amount':20,'attributes':{'1':{'name':'Pollo','ean13':'4006381333931'},'2':{'name':'24x85 gr','ean13':'4006381333931'}}}
  page=lambda:'<div data-product="'+html.escape(json.dumps(p),quote=True)+'">'
  v=verify_quantity(r,page());self.assertEqual(v['weight_kg'],2.04);self.assertTrue(v['quantity_verified'])
  p['price_amount']=21;self.assertFalse(verify_quantity(r,page())['quantity_verified'])
  p['price_amount']=20;p['attributes']['1']['ean13']='other';self.assertFalse(verify_quantity(r,page())['quantity_verified'])
 def test_reject_foreign_tracking_or_destination_and_duplicates(self):
  for replacement in ['tt=999_','r=https%3A%2F%2Fevil.example%2F']:
   f=fixture();f['products'][0]['URL']=f['products'][0]['URL'].replace('tt=24833_',replacement) if replacement.startswith('tt') else f['products'][0]['URL'].split('&r=')[0]+'&'+replacement
   with self.assertRaises(ValueError):normalize(f)
  f=fixture();f['products']*=2
  with self.assertRaises(ValueError):normalize(f)
 def test_invalid_price_not_published(self):
  f=fixture();f['products'][0]['price']['amount']=0
  with self.assertRaises(ValueError):normalize(f)
if __name__=='__main__':unittest.main()
