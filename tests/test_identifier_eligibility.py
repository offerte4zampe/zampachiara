import unittest
from automation.enrich_catalog import eligible_for_identifier_lookup

class IdentifierEligibilityTests(unittest.TestCase):
    def test_missing_mass_does_not_hide_accessories_or_volume_from_lookup(self):
        brands={'brand':{'webpet','animaliapet'}}
        for title in ['Shampoo 250 ml','Gioco per gatto','Snack 12 pezzi']:
            o=dict(merchant_id='webpet',brand='Brand',available=True,title=title,weight_kg=None)
            self.assertTrue(eligible_for_identifier_lookup(o,brands))
            for extra in [dict(available=False),dict(source_type='official_feed'),dict(merchant_id='paco'),dict(brand='Other')]:
                self.assertFalse(eligible_for_identifier_lookup(dict(o,**extra),brands))
