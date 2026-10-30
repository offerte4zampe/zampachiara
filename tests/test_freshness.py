import datetime as dt
import unittest
from automation.freshness import source_freshness, label, banner
from automation.build_home_data import build
from automation.build_catalog_preview import render_preview

NOW=dt.datetime(2026,10,30,12,tzinfo=dt.timezone.utc)

class FreshnessTests(unittest.TestCase):
    def test_failed_fetch_does_not_refresh_old_offers(self):
        source={'id':'shop','name':'Shop','status':'stale','checked_at':NOW.isoformat()}
        rows=[{'merchant_id':'shop','checked_at':'2026-10-29T22:00:00Z'}, {'merchant_id':'shop','checked_at':'2026-10-29T23:00:00Z'}]
        s=source_freshness(source,rows,NOW)
        self.assertEqual(s['checked_at'],'2026-10-29T23:00:00+00:00')
        self.assertEqual(s['attempted_at'],NOW.isoformat())
        self.assertEqual(s['freshness'],'stale')
        self.assertEqual(s['data_age_hours'],13)
        self.assertEqual(label(s['checked_at'],NOW),'Dati non aggiornati da 13 ore')
        html=banner('<div id="catalog-filters"></div>',[s],NOW)
        self.assertIn('Shop: Dati non aggiornati da 13 ore',html)
        self.assertNotIn('role="status" hidden',html)
        self.assertEqual(banner(html,[s],NOW),html)

    def test_threshold_invalid_and_future_timestamps(self):
        self.assertEqual(label('2026-10-30T00:00:00Z',NOW),'')
        self.assertEqual(label(None,NOW),'Data aggiornamento non disponibile')
        self.assertEqual(label('2026-10-30T13:00:00Z',NOW),'Data aggiornamento non disponibile')
        self.assertEqual(source_freshness({'id':'shop'},[],NOW)['freshness'],'unknown')

    def test_home_excludes_13_hour_offer_but_catalog_labels_it(self):
        row={'id':'shop:1','merchant_id':'shop','merchant':'Shop','title':'Cibo cane','brand':'Marca','price':10,'weight_kg':2,'available':True,'url':'https://shop.test/a','image':'https://shop.test/a.jpg','checked_at':'2026-10-29T23:00:00Z'}
        catalog={'offers':[row],'sources':[{'id':'shop','name':'Shop'}],'generated_at':NOW.isoformat(),'refresh_hours':6}
        self.assertEqual(build(catalog,NOW)['offers'],[])
        preview=render_preview('<div id="catalog-preview"></div>',catalog,NOW)
        self.assertIn('Dati non aggiornati da 13 ore',preview)
        self.assertIn('10,00',preview)
