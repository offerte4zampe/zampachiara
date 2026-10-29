"""Build attestation from an actual successful GitHub remote run, never repo state."""
import argparse,datetime as dt,hashlib,io,json,os,pathlib,re,subprocess,urllib.request,urllib.error,uuid,zipfile
try:
    from .d1_fingerprint import ROOT,input_hash,commit_sha,SCOPE
except ImportError:
    from d1_fingerprint import ROOT,input_hash,commit_sha,SCOPE
REPO='offerte4zampe/zampachiara'
OUTPUT=ROOT/'worker/generated/d1-validation.json'

def validate_remote_run(run,jobs):
    if run.get('event')!='workflow_dispatch' or run.get('head_branch')!='main' or run.get('status')!='completed' or run.get('conclusion')!='success':raise ValueError('Remote validation requires a successful manual run on main')
    if run.get('path')!='.github/workflows/d1-staging.yml' or run.get('repository',{}).get('full_name')!=REPO:raise ValueError('Unexpected workflow/repository')
    remote=[j for j in jobs if j.get('name')=='remote-staging']
    if len(remote)!=1 or remote[0].get('status')!='completed' or remote[0].get('conclusion')!='success':raise ValueError('remote-staging must be executed and successful; skipped is not valid')
    return {'remote_success':True,'remote_run_id':str(run['id']),'head_sha':run['head_sha'],'repository':REPO}

def headers():
    result={'Accept':'application/vnd.github+json','User-Agent':'Offerte4Zampe-D1-activation'}
    if os.environ.get('GITHUB_TOKEN'):result['Authorization']='Bearer '+os.environ['GITHUB_TOKEN']
    return result

def api(path):
    with urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/'+REPO+path,headers=headers()),timeout=20) as r:return json.load(r)

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):return None

def artifact_bytes(artifact_id):
    request=urllib.request.Request('https://api.github.com/repos/'+REPO+'/actions/artifacts/'+str(artifact_id)+'/zip',headers=headers())
    try:
        response=urllib.request.build_opener(NoRedirect).open(request,timeout=20)
    except urllib.error.HTTPError as error:
        if error.code not in (301,302,303,307,308):raise
        location=error.headers['Location']
        if not location.startswith('https://'):raise ValueError('Unsafe artifact redirect')
        # The GitHub credential must never follow the signed download redirect.
        response=urllib.request.urlopen(urllib.request.Request(location,headers={'User-Agent':'Offerte4Zampe-D1-activation'}),timeout=20)
    with response:data=response.read(5_000_001)
    if len(data)>5_000_000:raise ValueError('Unexpected artifact size')
    return data

class AttestationExpired(ValueError):pass

def validate_ancestry(verified_sha,current_sha,comparison=None):
    if verified_sha==current_sha:return True
    if not comparison or comparison.get('status')!='ahead' or comparison.get('merge_base_commit',{}).get('sha')!=verified_sha or comparison.get('base_commit',{}).get('sha')!=verified_sha:
        raise ValueError('Il commit attestato non è un antenato della build corrente')
    return True

def select_artifact(artifacts,run):
    matches=[a for a in artifacts if a.get('name')=='remote-d1-shipping-report']
    if not matches:raise ValueError('Attestazione non disponibile: artifact assente o eliminato dopo la retention; ripetere il workflow remoto')
    if len(matches)!=1:raise ValueError('Ambiguous workflow artifact')
    item=matches[0]
    until=item.get('expires_at')
    if item.get('expired') or (until and dt.datetime.fromisoformat(until.replace('Z','+00:00'))<=dt.datetime.now(dt.timezone.utc)):
        raise AttestationExpired('Attestazione scaduta: retention artifact terminata; ripetere il workflow remoto')
    origin=item.get('workflow_run',{})
    if str(origin.get('id'))!=str(run['id']) or origin.get('head_branch')!='main' or origin.get('head_sha')!=run['head_sha']:
        raise ValueError('Artifact di un altro run, ramo o commit')
    return item

def validate_attestation(record,run,sha,digest,ancestor_verified=False):
    validate_fields=('run_id','commit_sha','input_hash','verified_at','database_uuid','database_name','worker_name','execution','scope')
    if any(k not in record for k in validate_fields):raise ValueError('Incomplete remote attestation')
    if str(record['run_id'])!=str(run['id']) or record['commit_sha']!=run['head_sha']:raise ValueError('Remote attestation SHA/run differs from verified run')
    if record['commit_sha']!=sha and not ancestor_verified:raise ValueError('Ancestry verification is required for a newer build')
    if record['input_hash']!=digest:raise ValueError('Migrations/seed or verification code changed since the remote run')
    if record['scope']!=SCOPE:raise ValueError('Import validation is not infrastructure validation')
    if record['execution']!='remote-d1' or record['database_name']!='zampachiara-shipping-staging' or record['worker_name']!='zampachiara-d1-staging':raise ValueError('Attestation is not from the remote staging resources')
    if uuid.UUID(record['database_uuid']).int==0:raise ValueError('Invalid verified database UUID')
    date=dt.datetime.fromisoformat(record['verified_at'].replace('Z','+00:00'))
    if date.tzinfo is None or date>dt.datetime.now(dt.timezone.utc)+dt.timedelta(minutes=5):raise ValueError('Invalid verification timestamp')
    return {'remote_success':True,'attestation_scope':SCOPE,'ancestor_verified':True,'remote_run_id':str(run['id']),'remote_commit_sha':record['commit_sha'],'build_commit_sha':sha,'verified_input_hash':record['input_hash'],'current_input_hash':digest,'verified_at':record['verified_at'],'database_uuid':record['database_uuid']}

def verify(run_id,sha,digest):
    if not re.fullmatch(r'[1-9]\d*',str(run_id)):raise ValueError('Invalid remote run ID')
    run=api('/actions/runs/'+str(run_id))
    if str(run.get('id'))!=str(run_id):raise ValueError('API returned another run ID')
    jobs=[];page=1
    while True:
        result=api('/actions/runs/'+str(run_id)+'/jobs?filter=latest&per_page=100&page='+str(page));jobs+=result['jobs']
        if len(jobs)>=result['total_count']:break
        page+=1
    validate_remote_run(run,jobs)
    comparison=api('/compare/'+run['head_sha']+'...'+sha) if run['head_sha']!=sha else None
    validate_ancestry(run['head_sha'],sha,comparison)
    artifacts=api('/actions/runs/'+str(run_id)+'/artifacts?per_page=100')['artifacts']
    artifact=select_artifact(artifacts,run)
    try:data=artifact_bytes(artifact['id'])
    except urllib.error.HTTPError as error:
        if error.code==410:raise AttestationExpired('Attestazione scaduta: GitHub non rende più disponibile l’artifact; ripetere il workflow remoto') from None
        raise
    if artifact.get('digest')!='sha256:'+hashlib.sha256(data).hexdigest():raise ValueError('Artifact digest mismatch')
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        try:item=archive.getinfo('remote-d1-attestation.json')
        except KeyError:raise ValueError('Attestazione assente nell’artifact; ripetere il workflow remoto') from None
        if item.file_size>65536:raise ValueError('Unexpected attestation size')
        record=json.loads(archive.read(item))
    return validate_attestation(record,run,sha,digest,ancestor_verified=True)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-run');parser.add_argument('--prepare-build',action='store_true');args=parser.parse_args()
    # Generated evidence is never accepted as a tracked repository source.
    tracked=subprocess.run(['git','ls-files','--error-unmatch',str(OUTPUT.relative_to(ROOT))],cwd=ROOT,capture_output=True).returncode==0
    if tracked:raise ValueError('Generated attestation must not be committed to the repository')
    # Delete stale generated evidence before any validation that could fail.
    OUTPUT.unlink(missing_ok=True)
    if (ROOT/'worker/d1-validation.json').exists():raise ValueError('Repository proof files are not accepted; use the workflow artifact')
    config=json.loads((ROOT/'wrangler.jsonc').read_text());flags=config.get('vars',{})
    requested=flags.get('SHIPPING_RULES_SOURCE')=='d1' or flags.get('SHIPPING_SHADOW')=='true'
    sha=commit_sha();digest=input_hash();run_id=args.verify_run or os.environ.get('SHIPPING_D1_REMOTE_RUN_ID')
    if requested and not run_id:raise ValueError('D1/shadow requested without a remote run ID')
    if run_id:subprocess.run(['git','diff','--exit-code','HEAD','--'],cwd=ROOT,check=True,capture_output=True)
    result=verify(run_id,sha,digest) if run_id else {'remote_success':False,'remote_run_id':None,'build_commit_sha':sha,'current_input_hash':digest}
    if args.prepare_build:
        OUTPUT.parent.mkdir(parents=True,exist_ok=True);OUTPUT.write_text(json.dumps(result,indent=2)+'\n')
    print('Attestazione remota valida: input D1 invariati e commit attestato antenato della build.' if run_id else 'No remote attestation: build remains JSON; D1 and shadow blocked.')
if __name__=='__main__':main()
