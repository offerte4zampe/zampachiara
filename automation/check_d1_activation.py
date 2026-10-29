"""Validate actual successful remote jobs before preparing production activation.

No production flag or binding is changed. A skipped job is never evidence.
"""
import argparse,json,os,pathlib,re,urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
REPO='offerte4zampe/zampachiara'
PROOF=ROOT/'worker/d1-validation.json'

def validate_remote_run(run,jobs):
    if run.get('event')!='workflow_dispatch' or run.get('head_branch')!='main' or run.get('status')!='completed' or run.get('conclusion')!='success':raise ValueError('Remote validation requires a successful manual run on main')
    if run.get('path')!='.github/workflows/d1-staging.yml' or run.get('repository',{}).get('full_name')!=REPO:raise ValueError('Unexpected workflow/repository')
    remote=[j for j in jobs if j.get('name')=='remote-staging']
    if len(remote)!=1 or remote[0].get('status')!='completed' or remote[0].get('conclusion')!='success':raise ValueError('remote-staging must be executed and successful; skipped is not valid')
    return {'remote_success':True,'remote_run_id':str(run['id']),'head_sha':run['head_sha'],'repository':REPO}

def api(path):
    headers={'Accept':'application/vnd.github+json','User-Agent':'Offerte4Zampe-D1-activation'}
    token=os.environ.get('GITHUB_TOKEN')
    if token:headers['Authorization']='Bearer '+token
    with urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/'+REPO+path,headers=headers),timeout=20) as r:return json.load(r)

def verify(run_id):
    if not re.fullmatch(r'[1-9]\d*',str(run_id)):raise ValueError('Invalid remote run ID')
    run=api('/actions/runs/'+str(run_id));jobs=[];page=1
    while True:
        result=api('/actions/runs/'+str(run_id)+'/jobs?filter=latest&per_page=100&page='+str(page));jobs+=result['jobs']
        if len(jobs)>=result['total_count']:break
        page+=1
    return validate_remote_run(run,jobs)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-run');parser.add_argument('--write-proof',action='store_true');args=parser.parse_args()
    config=json.loads((ROOT/'wrangler.jsonc').read_text());proof=json.loads(PROOF.read_text());flags=config.get('vars',{})
    requested=flags.get('SHIPPING_RULES_SOURCE')=='d1' or flags.get('SHIPPING_SHADOW')=='true'
    if args.write_proof and not args.verify_run:raise ValueError('--write-proof requires --verify-run')
    if args.verify_run:
        checked=verify(args.verify_run)
        if args.write_proof:PROOF.write_text(json.dumps(checked,indent=2)+'\n')
        print('Remote run executed and successful; production remains unchanged.');return
    if not requested and not proof.get('remote_success'):
        print('D1 activation NOT requested; production remains JSON, shadow disabled.');return
    if not proof.get('remote_success'):raise ValueError('D1/shadow requested without successful remote validation')
    checked=verify(proof.get('remote_run_id'))
    if checked!=proof:raise ValueError('Remote validation proof does not match GitHub run')
    print('Remote validation confirmed; activation flags may be reviewed separately.')
if __name__=='__main__':main()
