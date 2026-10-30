import unittest
from automation.enrich_catalog import lookup_priority

class LookupPriorityTests(unittest.TestCase):
    def test_missing_code_precedes_known_page_even_with_lower_name_score(self):
        self.assertLess(lookup_priority([{'gtin':''}], .1),
                        lookup_priority([{'gtin':'4006381333931'}], 1))
    def test_peer_similarity_then_number_of_missing_variants(self):
        self.assertLess(lookup_priority([{}], .9), lookup_priority([{},{}], .5))
        self.assertLess(lookup_priority([{},{}], .9), lookup_priority([{}], .9))
    def test_invalid_code_does_not_count_as_known(self):
        self.assertEqual(lookup_priority([{'gtin':'invalid'}]), lookup_priority([{}]))
