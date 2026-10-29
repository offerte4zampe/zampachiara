import copy,datetime as dt,json,pathlib,tempfile,unittest
from automation.check_d1_activation import validate_attestation
from automation.d1_fingerprint import input_hash,FILES

class VersionAttestationTests(unittest.TestCase):
 def setUp(self):
  self.run={'id':123,'head_sha':'commit-123'}
  self.record={'execution':'remote-d1','run_id':'123','commit_sha':'commit-123','input_hash':'hash-123','verified_at':dt.datetime.now(dt.timezone.utc).isoformat(),'database_uuid':'11111111-1111-4111-8111-111111111111','database_name':'zampachiara-shipping-staging','worker_name':'zampachiara-d1-staging'}
 def check(self,record=None,sha='commit-123',digest='hash-123'):
  return validate_attestation(record or self.record,self.run,sha,digest)
 def test_exact_sha_hash_date_and_database_are_preserved(self):
  result=self.check();self.assertTrue(result['remote_success']);self.assertEqual(result['database_uuid'],self.record['database_uuid']);self.assertEqual(result['verified_at'],self.record['verified_at'])
 def test_stale_commit_or_input_hash_cannot_authorize_current_build(self):
  for sha,digest in [('changed','hash-123'),('commit-123','changed')]:
   with self.assertRaises(ValueError):self.check(sha=sha,digest=digest)
 def test_mismatched_run_local_execution_database_and_date_are_rejected(self):
  for key,value in [('run_id','124'),('execution','local-workerd'),('database_uuid','00000000-0000-0000-0000-000000000000'),('database_name','production'),('worker_name','zampachiara'),('verified_at','invalid')]:
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
  record={'run_id':'123','commit_sha':'commit-123','input_hash':'hash-123','verified_at':now,'database_uuid':'11111111-1111-4111-8111-111111111111','database_name':'zampachiara-shipping-staging','worker_name':'zampachiara-d1-staging','execution':'remote-d1'}
  stream=io.BytesIO()
  with zipfile.ZipFile(stream,'w') as z:z.writestr('remote-d1-attestation.json',json.dumps(record))
  archive=stream.getvalue();artifact={'id':1,'name':'remote-d1-shipping-report','expired':False,'digest':'sha256:'+hashlib.sha256(archive).hexdigest()}
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
