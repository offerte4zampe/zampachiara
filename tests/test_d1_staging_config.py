import json,pathlib,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class StagingConfigTests(unittest.TestCase):
 def test_migration_is_identical_to_reviewed_schema(self):
  self.assertEqual((ROOT/'worker/staging/migrations/0001_shipping_rules.sql').read_bytes(),(ROOT/'worker/schema/0002_shipping_rules.sql').read_bytes())
 def test_staging_has_a_separate_name_binding_and_no_production_routes(self):
  c=json.loads((ROOT/'wrangler.staging.jsonc').read_text())
  self.assertEqual(c['name'],'zampachiara-d1-staging');self.assertEqual(c['routes'],[])
  self.assertEqual(c['d1_databases'][0]['binding'],'SHIPPING_DB_STAGING')
  self.assertEqual(c['d1_databases'][0]['database_name'],'zampachiara-shipping-staging')
  self.assertEqual(c['vars']['SHIPPING_RULES_SOURCE'],'json');self.assertEqual(c['vars']['SHIPPING_SHADOW'],'false')
