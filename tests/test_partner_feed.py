import sys,unittest,datetime as dt
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'automation'))
from import_partner_feed import merge
class FeedTest(unittest.TestCase):
 def setUp(self):
  self.now=dt.datetime(2026,10,18,tzinfo=dt.timezone.utc)
  self.feed={'merchant_id':'arcaplanet','checked_at':self.now.isoformat(),'source_type':'official_feed','offers':[{'id':'1','title':'Test fixture','url':'https://www.arcaplanet.it/product','price':10,'available':False}]}
  self.catalog={'offers':[{'id':'other:1','merchant_id':'other'},{'id':'arcaplanet:old','merchant_id':'arcaplanet'}],'sources':[]}
 def test_replace_snapshot_and_keep_out_of_stock(self):
  r=merge(self.catalog,self.feed,self.now);self.assertEqual([x['id'] for x in r['offers']],['other:1','arcaplanet:1']);self.assertFalse(r['offers'][-1]['available']);self.assertIsNone(r['offers'][-1]['weight_kg'])
 def test_stale_rejected_without_mutation(self):
  self.feed['checked_at']='2026-10-01T00:00:00+00:00'
  with self.assertRaises(ValueError):merge(self.catalog,self.feed,self.now)
  self.assertEqual(len(self.catalog['offers']),2)
 def test_foreign_url_rejected(self):
  self.feed['offers'][0]['url']='https://arcaplanet.it.example.org/p'
  with self.assertRaises(ValueError):merge(self.catalog,self.feed,self.now)
 def test_unknown_stock_rejected(self):
  self.feed['offers'][0]['available']='yes'
  with self.assertRaises(ValueError):merge(self.catalog,self.feed,self.now)
