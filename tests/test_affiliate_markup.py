import unittest
from automation.remove_unverified_ads import apply
class AffiliateMarkupTests(unittest.TestCase):
    def test_outbound_and_affiliate_rel_preserves_exact_href(self):
        for href in ['/go/shop%3A1?from=product','https://tc.tradetracker.net/?c=1&amp;a=2','https://www.amazon.it/dp/B012345678?tag=exact-21']:
            result=apply('<a href="'+href+'">Compra</a>')
            self.assertIn('href="'+href+'"',result)
            self.assertIn('rel="sponsored nofollow noopener noreferrer"',result)
            self.assertIn('target="_blank"',result)
            self.assertEqual(result,apply(result))
        direct='<a href="https://example.test/help">Fonte</a>'
        self.assertEqual(apply(direct),direct)
