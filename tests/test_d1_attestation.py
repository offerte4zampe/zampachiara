import copy,datetime as dt,json,pathlib,tempfile,unittest
from automation.check_d1_activation import validate_attestation,validate_ancestry,select_artifact,AttestationExpired
from automation.d1_fingerprint import input_hash,FILES

class VersionAttestationTests(unittest.TestCase):
 def setUp(self):
  self.run={'id':123,'head_sha':'commit-123'}
  self.record={'scope':'shipping-infrastructure-v1','execution':'remote-d1','run_id':'123','commit_sha':'commit-123','input_hash':'hash-123','verified_at':dt.datetime.now(dt.timezone.utc).isoformat(),'database_uuid':'11111111-1111-4111-8111-111111111111','database_name':'zampachiara-shipping-staging','worker_name':'zampachiara-d1-staging'}
 def check(self,record=None,sha='commit-123',digest='hash-123'):
  return validate_attestation(record or self.record,self.run,sha,digest)
 def test_exact_sha_hash_date_and_database_are_preserved(self):
  result=self.check();self.assertTrue(result['remote_success']);self.assertEqual(result['database_uuid'],self.record['database_uuid']);self.assertEqual(result['verified_at'],self.record['verified_at'])
 def test_stale_commit_or_input_hash_cannot_authorize_current_build(self):
  for sha,digest in [('changed','hash-123'),('commit-123','changed')]:
   with self.assertRaises(ValueError):self.check(sha=sha,digest=digest)
 def test_mismatched_run_local_execution_database_and_date_are_rejected(self):
  for key,value in [('run_id','124'),('scope','product-offer-import-v1'),('execution','local-workerd'),('database_uuid','00000000-0000-0000-0000-000000000000'),('database_name','production'),('worker_name','zampachiara'),('verified_at','invalid')]:
   with self.assertRaises(ValueError):self.check({**self.record,key:value})
 def test_missing_record_fields_are_rejected(self):
  for key in self.record:
   record=copy.deepcopy(self.record);del record[key]
   with self.assertRaises(ValueError):self.check(record)
 def test_migration_addition_seed_and_source_edits_change_fingerprint(self):
  with tempfile.TemporaryDirectory() as folder:
   root=pathlib.Path(folder)
   for name in FILES:
    path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text('fixture')
   migrations=root/'worker/staging/migrations';migrations.mkdir(parents=True)
   initial=input_hash(root);(migrations/'0001.sql').write_text('CREATE TABLE a(id);');self.assertNotEqual(initial,input_hash(root))
   before=input_hash(root);seed=root/'worker/seeds/shipping-rules.sql';seed.write_text('changed seed');self.assertNotEqual(before,input_hash(root))
   before=input_hash(root);(root/'site/data/shipping-rules.json').write_text('{}');self.assertNotEqual(before,input_hash(root))

class ArtifactTrustTests(unittest.TestCase):
 def fixture(self):
  import io,zipfile,hashlib
  now=dt.datetime.now(dt.timezone.utc).isoformat()
  run={'id':123,'head_sha':'commit-123','event':'workflow_dispatch','head_branch':'main','status':'completed','conclusion':'success','path':'.github/workflows/d1-staging.yml','repository':{'full_name':'offerte4zampe/zampachiara'}}
  record={'run_id':'123','commit_sha':'commit-123','input_hash':'hash-123','verified_at':now,'database_uuid':'11111111-1111-4111-8111-111111111111','database_name':'zampachiara-shipping-staging','worker_name':'zampachiara-d1-staging','scope':'shipping-infrastructure-v1','execution':'remote-d1'}
  stream=io.BytesIO()
  with zipfile.ZipFile(stream,'w') as z:z.writestr('remote-d1-attestation.json',json.dumps(record))
  archive=stream.getvalue();artifact={'id':1,'name':'remote-d1-shipping-report','expired':False,'digest':'sha256:'+hashlib.sha256(archive).hexdigest(),'workflow_run':{'id':123,'head_branch':'main','head_sha':'commit-123'},'expires_at':(dt.datetime.now(dt.timezone.utc)+dt.timedelta(days=1)).isoformat()}
  jobs={'total_count':1,'jobs':[{'name':'remote-staging','status':'completed','conclusion':'success'}]}
  return run,jobs,{'artifacts':[artifact]},archive
 def test_api_and_digest_are_checked_not_a_repository_success_flag(self):
  from unittest.mock import patch
  from automation.check_d1_activation import verify
  run,jobs,artifacts,data=self.fixture()
  with patch('automation.check_d1_activation.api',side_effect=[run,jobs,artifacts]),patch('automation.check_d1_activation.artifact_bytes',return_value=data):
   self.assertTrue(verify('123','commit-123','hash-123')['remote_success'])
  with patch('automation.check_d1_activation.api',side_effect=[run,jobs,artifacts]),patch('automation.check_d1_activation.artifact_bytes',return_value=data+b'tampered'):
   with self.assertRaisesRegex(ValueError,'digest'):verify('123','commit-123','hash-123')
 def test_an_actual_skipped_job_is_rejected_before_reading_any_artifact(self):
  from unittest.mock import patch
  from automation.check_d1_activation import verify
  run,jobs,_,_=self.fixture();jobs['jobs'][0]['conclusion']='skipped'
  with patch('automation.check_d1_activation.api',side_effect=[run,jobs]),patch('automation.check_d1_activation.artifact_bytes') as download:
   with self.assertRaisesRegex(ValueError,'executed'):verify('123','commit-123','hash-123')
   download.assert_not_called()


class AncestryPolicyTests(unittest.TestCase):
 def test_equal_and_descendant_commits_are_accepted_but_divergent_are_not(self):
  self.assertTrue(validate_ancestry('old','old'))
  self.assertTrue(validate_ancestry('old','new',{'status':'ahead','base_commit':{'sha':'old'},'merge_base_commit':{'sha':'old'}}))
  for comparison in [None,{'status':'behind'},{'status':'diverged'},{'status':'ahead','base_commit':{'sha':'old'},'merge_base_commit':{'sha':'other'}}]:
   with self.assertRaises(ValueError):validate_ancestry('old','new',comparison)
 def test_catalog_snapshots_are_neutral_but_shipping_rules_and_config_are_not(self):
  with tempfile.TemporaryDirectory() as folder:
   root=pathlib.Path(folder)
   for name in FILES:
    p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('fixture')
   initial=input_hash(root)
   for name in ['site/data/catalog.json.gz','site/data/home.json','site/data/canonical-products/00.json','automation/product-registry.json']:
    p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('updated snapshot')
   self.assertEqual(initial,input_hash(root))
   for name in ['site/data/shipping-rules.json','wrangler.jsonc','worker/shipping-source.mjs']:
    p=root/name;before=input_hash(root);p.write_text('changed D1 input');self.assertNotEqual(before,input_hash(root))
 def test_expiration_and_wrong_run_branch_sha_are_explicitly_rejected(self):
  run={'id':123,'head_sha':'old'};item={'name':'remote-d1-shipping-report','expired':False,'workflow_run':{'id':123,'head_branch':'main','head_sha':'old'}}
  self.assertEqual(select_artifact([item],run),item)
  for origin in [{'id':124,'head_branch':'main','head_sha':'old'},{'id':123,'head_branch':'feature','head_sha':'old'},{'id':123,'head_branch':'main','head_sha':'other'}]:
   with self.assertRaisesRegex(ValueError,'altro run'):select_artifact([{**item,'workflow_run':origin}],run)
  for expired in [{**item,'expired':True},{**item,'expires_at':'2020-01-01T00:00:00Z'}]:
   with self.assertRaisesRegex(AttestationExpired,'Attestazione scaduta'):select_artifact([expired],run)
 def test_full_verification_checks_compare_api_for_catalog_descendant(self):
  from unittest.mock import patch
  from automation.check_d1_activation import verify
  run,jobs,artifacts,data=ArtifactTrustTests().fixture()
  comparison={'status':'ahead','base_commit':{'sha':run['head_sha']},'merge_base_commit':{'sha':run['head_sha']}}
  with patch('automation.check_d1_activation.api',side_effect=[run,jobs,comparison,artifacts]) as api,patch('automation.check_d1_activation.artifact_bytes',return_value=data):
   result=verify('123','new-catalog-sha','hash-123');self.assertTrue(result['ancestor_verified']);self.assertEqual(result['build_commit_sha'],'new-catalog-sha');self.assertEqual(api.call_args_list[2].args[0],'/compare/commit-123...new-catalog-sha')
 def test_run_api_cannot_return_another_id(self):
  from unittest.mock import patch
  from automation.check_d1_activation import verify
  with patch('automation.check_d1_activation.api',return_value={'id':124}):
   with self.assertRaisesRegex(ValueError,'another run ID'):verify('123','new','hash')
