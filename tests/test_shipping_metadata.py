import datetime as dt
import json
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parents[1]/'automation'))
from shipping_metadata import supplement
class ShippingMetadata(unittest.TestCase):
 def test_exact_variant_only_and_no_price_or_net_weight_overwrite(self):
  with tempfile.TemporaryDirectory() as tmp:
   rows=[dict(id='bauzaar:1',price=10,weight_kg=1),dict(id='bauzaar:2',price=20,weight_kg=2)]
   public=[dict(id='bauzaar:1',price=99,weight_kg=99,shipping_weight_kg=1.2)]
   supplement(rows,lambda:(public,{'status':'ok'}),Path(tmp)/'cache.json')
   self.assertEqual(rows[0]['shipping_weight_kg'],1.2);self.assertEqual(rows[0]['price'],10);self.assertEqual(rows[0]['weight_kg'],1)
   self.assertNotIn('shipping_weight_kg',rows[1])
 def test_failed_refresh_does_not_make_old_weight_fresh(self):
  now=dt.datetime(2026,10,19,tzinfo=dt.timezone.utc)
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'cache.json';p.write_text(json.dumps(dict(checked_at='2026-10-01T00:00:00+00:00',weights={'a':12})))
   rows=[dict(id='a')];supplement(rows,lambda:([],{'status':'error'}),p,now)
   self.assertNotIn('shipping_weight_kg',rows[0]);self.assertIn('2026-10-01',p.read_text())
