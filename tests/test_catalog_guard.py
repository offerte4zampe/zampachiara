import copy
import datetime
import unittest
from automation.guard_catalog import check

NOW = datetime.datetime(2026, 10, 20, 8, tzinfo=datetime.timezone.utc)
BASE = dict(id='a', title='Ricetta', variant='2 kg', brand='Marca', merchant='A', merchant_id='a', price=10,
            weight_kg=2, available=True, gtin='4006381333931', url='https://shop.example/product', checked_at='2026-10-20T07:00:00Z')


class GuardTests(unittest.TestCase):
    def test_only_independent_agreeing_exact_format_peers_can_suspend(self):
        rows = [dict(BASE, price=2), dict(BASE, id='b', merchant_id='b', price=10), dict(BASE, id='c', merchant_id='c', price=11)]
        clean, report = check({'offers': rows}, NOW)
        self.assertEqual([o['id'] for o in clean['offers']], ['b', 'c'])
        self.assertEqual(report['quarantined'][0]['reasons'], ['exact_product_peer_outlier_pending_review'])
        for patch in [dict(weight_kg=4), dict(brand='Other'), dict(gtin='4006381333932'), dict(merchant_id='b'), dict(price=20)]:
            different = copy.deepcopy(rows);different[2].update(patch)
            clean, _ = check({'offers': different}, NOW)
            self.assertIn('a', [o['id'] for o in clean['offers']])

    def test_invalid_prices_links_dates_and_duplicate_ids_are_not_published(self):
        for patch in [dict(price=float('nan')), dict(price=0), dict(url='javascript:alert(1)'), dict(url='https://user:pass@shop.example'), dict(checked_at='2026-10-10'), dict(checked_at='2026-10-21T00:00:00Z')]:
            clean, _ = check({'offers': [dict(BASE, **patch)]}, NOW)
            self.assertEqual(clean['offers'], [])
        clean, _ = check({'offers': [BASE, dict(BASE, price=11)]}, NOW)
        self.assertEqual(clean['offers'], [])

    def test_bad_weight_is_removed_without_inventing_price_or_altering_input(self):
        offer = dict(BASE, weight_kg=-2, shipping_weight_kg=float('inf'))
        clean, report = check({'offers': [offer]}, NOW)
        self.assertIsNone(clean['offers'][0]['weight_kg'])
        self.assertIsNone(clean['offers'][0]['shipping_weight_kg'])
        self.assertEqual(clean['offers'][0]['price'], 10)
        self.assertEqual(offer['weight_kg'], -2)
        self.assertEqual(len(report['repaired']), 2)
