import unittest,importlib.util,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]/'automation'))
from enrich_catalog import gtin
from update_history import update
class TrustTests(unittest.TestCase):
 def test_barcode_checksum(self):
  self.assertEqual(gtin('4006381333931'),'04006381333931')
  for code in ['4006381333932','not-a-code','0000000000000','123']:self.assertEqual(gtin(code),'')
 def test_real_daily_range_no_duplicate_or_stale_backfill(self):
  o={'id':'a','price':10,'available':True,'checked_at':'2026-10-18T08:00:00Z'}
  cat={'generated_at':'2026-10-18T08:00:00Z','offers':[o]}
  h=update({},cat,'2026-10-18');o['price']=12;h=update(h,cat,'2026-10-18');self.assertEqual(len(h['offers']['a']),1);self.assertEqual(h['offers']['a'][0]['low'],10);self.assertEqual(h['offers']['a'][0]['high'],12)
  h=update(h,cat,'2026-10-19');self.assertEqual(len(h['offers']['a']),1)
