import datetime as dt
import unittest
from automation.display_time import format_timestamp
from automation.apply_micro_fixes import apply
from automation.build_home_data import build

class DisplayTimeTests(unittest.TestCase):
    def test_rome_summer_winter_and_date_precision(self):
        self.assertEqual(format_timestamp('2026-07-01T12:00:00Z'),'01/07/2026, 14:00')
        self.assertEqual(format_timestamp('2026-01-01T12:00:00Z'),'01/01/2026, 13:00')
        self.assertEqual(format_timestamp('2026-10-30'),'30/10/2026')
        self.assertEqual(format_timestamp(None),'non disponibile')

    def test_text_conversion_preserves_machine_timestamps_and_scripts(self):
        html='<time datetime="2026-07-01T12:00:00Z">2026-07-01T12:00:00Z</time><p>2026-07-01 12:00 UTC · 1 ore fa</p><script type="application/json">{"checked_at":"2026-07-01T12:00:00Z"}</script><label><input id="catalog-sale"> Sconti verificati · non disponibili</label>'
        out=apply(html)
        self.assertIn('datetime="2026-07-01T12:00:00Z"',out)
        self.assertIn('>01/07/2026, 14:00</time>',out)
        self.assertIn('01/07/2026, 14:00 · 1 ora fa',out)
        self.assertIn('{"checked_at":"2026-07-01T12:00:00Z"}',out)
        self.assertIn('<label hidden style="display:none">',out)
        self.assertEqual(apply(out),out)

    def test_store_counts_and_home_total_use_same_snapshot(self):
        now=dt.datetime(2026,10,30,tzinfo=dt.timezone.utc)
        offers=[{'id':str(i),'merchant_id':shop,'url':'https://shop.test/a','available':True,'price':10,'title':'Food','brand':'Marca','checked_at':now.isoformat()} for i,shop in enumerate(['a','a','b'])]
        catalog={'offers':offers,'sources':[{'id':'a','offers':999},{'id':'b','offers':777}],'generated_at':now.isoformat(),'refresh_hours':6}
        home=build(catalog,now)
        self.assertEqual([s['offers'] for s in home['sources']],[2,1])
        self.assertEqual(sum(s['offers'] for s in home['sources']),home['stats']['offers'])
        self.assertEqual(catalog['sources'][0]['offers'],999)
