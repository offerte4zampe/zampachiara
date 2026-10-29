import copy,unittest
from automation.check_d1_activation import validate_remote_run,REPO
from automation.verify_d1_staging import validate_staging_config,validate_resolved_database,validate_worker_url

class D1GuardTests(unittest.TestCase):
 def setUp(self):
  self.run={'id':123,'event':'workflow_dispatch','head_branch':'main','status':'completed','conclusion':'success','path':'.github/workflows/d1-staging.yml','repository':{'full_name':REPO},'head_sha':'abc'}
  self.jobs=[{'name':'remote-staging','status':'completed','conclusion':'success'}]
 def test_only_executed_successful_remote_job_is_accepted(self):
  self.assertTrue(validate_remote_run(self.run,self.jobs)['remote_success'])
  for conclusion in ('skipped','failure','cancelled',None):
   with self.assertRaises(ValueError):validate_remote_run(self.run,[{**self.jobs[0],'conclusion':conclusion}])
  with self.assertRaises(ValueError):validate_remote_run(self.run,[])
 def test_wrong_branch_event_and_workflow_are_rejected(self):
  for field,value in [('head_branch','feature'),('event','pull_request'),('status','in_progress'),('conclusion','failure'),('path','.github/workflows/basket-browser.yml')]:
   with self.assertRaises(ValueError):validate_remote_run({**self.run,field:value},self.jobs)
  with self.assertRaises(ValueError):validate_remote_run({**self.run,'repository':{'full_name':'another/repo'}},self.jobs)
 def test_database_name_and_actual_uuid_must_both_match(self):
  uid='11111111-1111-4111-8111-111111111111'
  validate_resolved_database({'name':'zampachiara-shipping-staging','uuid':uid},uid)
  for info in ({'name':'production','uuid':uid},{'name':'zampachiara-shipping-staging','uuid':'other'}):
   with self.assertRaises(RuntimeError):validate_resolved_database(info,uid)
 def test_worker_name_binding_and_routes_are_exact_not_suffix_only(self):
  c={'name':'zampachiara-d1-staging','routes':[],'d1_databases':[{'database_name':'zampachiara-shipping-staging','binding':'SHIPPING_DB_STAGING'}]};validate_staging_config(c)
  for field,value in [('name','zampachiara'),('routes',[{'pattern':'offerte4zampe.it'}])]:
   with self.assertRaises(RuntimeError):validate_staging_config({**c,field:value})
  wrong=copy.deepcopy(c);wrong['d1_databases'][0]['database_name']='unrelated-staging'
  with self.assertRaises(RuntimeError):validate_staging_config(wrong)
  validate_worker_url('https://zampachiara-d1-staging.example.workers.dev')
  for url in ('https://zampachiara.example.workers.dev','https://zampachiara-d1-staging.example.workers.dev.attacker.test'):
   with self.assertRaises(RuntimeError):validate_worker_url(url)
