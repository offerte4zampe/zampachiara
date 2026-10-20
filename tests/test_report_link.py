import unittest
from automation.report_link import error_link


class ReportLinks(unittest.TestCase):
    def test_report_contains_only_public_offer_context(self):
        link=error_link(dict(id='a',title='Food <test>',merchant='Shop',price=10,checked_at='2026-10-20',affiliate_url='https://tracking.example/private',email='private@example.com'))
        self.assertIn('segnala-errore.html?',link)
        self.assertNotIn('<test>',link)
        self.assertNotIn('tracking.example',link)
        self.assertNotIn('private@example',link)
