import unittest
from automation.build_home_data import search_index

class SearchIndexTests(unittest.TestCase):
    def test_names_and_freshness_without_prices_or_commercial_payload(self):
        source={'generated_at':'2026-10-20', 'offers':[{'id':'offer-1','title':'Cibo cane','variant':'2 kg','available':True,'checked_at':'2026-10-20','price':99,'image':'x','affiliate_url':'secret','url':'shop','description':'long'}]}
        result=search_index(source)
        self.assertEqual(result['offers'],[{'id':'offer-1','title':'Cibo cane','variant':'2 kg','available':True,'checked_at':'2026-10-20'}])
        self.assertEqual(source['offers'][0]['price'],99)

    def test_no_fabricated_availability_or_timestamp(self):
        result=search_index({'offers':[{'title':'Solo nome'},{'title':None}]})
        self.assertEqual(result['offers'],[{'title':'Solo nome'}])
