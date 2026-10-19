import datetime
import unittest
from automation.build_home_data import build


class HomeDataTests(unittest.TestCase):
    def test_small_payload_keeps_prices_and_excludes_stale_or_suspicious_deals(self):
        now = datetime.datetime(2026, 10, 19, tzinfo=datetime.timezone.utc)
        base = dict(id='ok', merchant_id='shop', merchant='Shop', brand='Brand', title='Food', price=10, previous_price=20, image='https://example.com/a.jpg', url='https://example.com/product', available=True, checked_at=now.isoformat())
        offers = [base, base | dict(id='stale', checked_at='2026-10-16T00:00:00+00:00'), base | dict(id='suspicious', previous_price=100), base | dict(id='out', available=False)]
        result = build(dict(offers=offers, sources=[dict(id='shop')], generated_at=now.isoformat(), refresh_hours=6), now)
        self.assertEqual([o['id'] for o in result['offers']], ['ok'])
        self.assertEqual(result['offers'][0]['price'], 10)
        self.assertEqual(result['stats']['offers'], 4)
        self.assertNotIn('affiliate_url', result['offers'][0])
