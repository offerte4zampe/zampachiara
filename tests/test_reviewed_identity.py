import copy
import datetime as dt
import json
import unittest
from pathlib import Path
from automation.reviewed_identity import apply


class ReviewedIdentityTests(unittest.TestCase):
    def setUp(self):
        self.review = json.loads((Path(__file__).parents[1]/'automation/reviewed-identities.json').read_text())[0]
        self.rows = [{**m, 'weight_kg': .03, 'gtin': self.review['gtin'] if m['id'] == self.review['reference_id'] else ''} for m in self.review['offers']]
        self.now = dt.datetime(2026, 10, 28, 15, tzinfo=dt.timezone.utc)

    def test_review_preserves_prices_and_marks_inferred_identifier(self):
        self.rows[1]['price'] = 40.69
        self.assertEqual(apply(self.rows, [self.review], self.now), 1)
        self.assertEqual(self.rows[1]['gtin'], self.review['gtin'])
        self.assertEqual(self.rows[1]['price'], 40.69)
        self.assertTrue(self.rows[1]['gtin_source'].startswith('reviewed:'))
        self.assertEqual(apply(self.rows, [self.review], self.now), 1)

    def test_changed_format_title_url_reference_or_conflicting_code_fail_closed(self):
        for key, value in [('title', 'Fortiflora Chews 30 pz'), ('weight_kg', .007), ('url', 'https://shop.test/other'), ('gtin', '4006381333931'), ('quantity_verified', False)]:
            rows=copy.deepcopy(self.rows);rows[1][key]=value
            self.assertEqual(apply(rows,[self.review],self.now),0)
        rows=copy.deepcopy(self.rows);rows[0]['gtin']=''
        self.assertEqual(apply(rows,[self.review],self.now),0)

    def test_expired_review_is_removed_including_previously_inferred_code(self):
        apply(self.rows,[self.review],self.now)
        self.assertEqual(apply(self.rows,[self.review],self.now+dt.timedelta(days=100)),0)
        self.assertEqual(self.rows[1]['gtin'],'')
        self.assertNotIn('identity_review',self.rows[1])
