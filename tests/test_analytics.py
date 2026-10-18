import sys,unittest,datetime as dt
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'automation'))
from read_analytics import period,summarize
class AnalyticsTest(unittest.TestCase):
 def test_rome_day_and_dst(self):
  start,end=period('2026-10-25',dt.datetime(2026,10,27,tzinfo=dt.timezone.utc));self.assertEqual((end-start).total_seconds(),25*3600)
 def test_today_is_partial(self):
  now=dt.datetime(2026,10,18,17,tzinfo=dt.timezone.utc);a,b=period('2026-10-18',now);self.assertEqual(b,now);self.assertEqual(a.hour,22);self.assertEqual(a.day,17)
 def test_no_data_is_not_zero(self):
  a,b=period('2026-10-18',dt.datetime(2026,10,19,tzinfo=dt.timezone.utc));r=summarize({'data':{'viewer':{'zones':[{'httpRequestsAdaptiveGroups':[]}]}}},a,b);self.assertIsNone(r['requests']);self.assertEqual(r['status'],'no_data')
 def test_graphql_error_not_zero(self):
  with self.assertRaises(ValueError):summarize({'errors':[{'message':'denied'}]},None,None)
