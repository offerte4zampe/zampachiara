import datetime
import unittest
from automation.build_catalog_preview import render_preview

NOW = datetime.datetime(2026, 10, 21, tzinfo=datetime.timezone.utc)


class PreviewTests(unittest.TestCase):
    def catalog(self):
        return {'generated_at': NOW.isoformat(), 'refresh_hours': 6,
                'sources': [{'id': 'shop', 'name': 'Shop', 'offers': 1}],
                'offers': [{'id': 'one', 'title': 'Cibo gatti <test>', 'brand': 'Marca',
                            'merchant': 'Shop', 'merchant_id': 'shop', 'price': 12.5,
                            'variant': '2 kg', 'weight_kg': 2, 'image': 'https://shop.test/a.jpg',
                            'url': 'https://shop.test/item', 'affiliate_url': 'https://tc.tradetracker.net/?c=1&a=2',
                            'available': True, 'checked_at': NOW.isoformat()}]}

    def test_real_price_format_tracking_and_idempotence(self):
        catalog = self.catalog()
        html = '<div id="catalog-preview"></div><div id="catalog-grid"></div>'
        out = render_preview(html, catalog, NOW)
        self.assertIn('12,50 €', out)
        self.assertIn('6,25 €/kg', out)
        self.assertIn('Cibo gatti &lt;test&gt;', out)
        self.assertIn('c=1&amp;a=2', out)
        self.assertIn('rel="sponsored noopener noreferrer"', out)
        self.assertIn('spedizione esclusa', out)
        self.assertEqual(render_preview(out, catalog, NOW), out)

    def test_no_stale_or_unavailable_price(self):
        catalog = self.catalog()
        catalog['offers'][0]['checked_at'] = '2026-10-01T00:00:00+00:00'
        out = render_preview('<div id="catalog-preview"></div>', catalog, NOW)
        self.assertNotIn('12,50', out)
        self.assertIn('Nessuna selezione recente', out)
        catalog['offers'][0]['checked_at'] = NOW.isoformat()
        catalog['offers'][0]['available'] = False
        self.assertNotIn('12,50', render_preview('<div id="catalog-preview"></div>', catalog, NOW))
