"""Version fingerprint of every reviewed input to the D1 shipping verification."""
import hashlib,pathlib,subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
SCOPE='shipping-infrastructure-v1'
FILES=(
 '.github/workflows/d1-staging.yml','.github/workflows/d1-activation.yml','wrangler.staging.jsonc','wrangler.jsonc',
 'automation/d1_fingerprint.py','automation/build_shipping_seed.py','automation/verify_d1_staging.py','automation/check_d1_activation.py',
 'site/data/shipping-rules.json','site/assets/trade.js','site/assets/catalog-metadata.js',
 'worker/index.mjs','worker/canonical-product.mjs','worker/shipping-source.mjs','worker/staging-shipping.mjs','worker/staging/shipping-matrix.mjs',
 'worker/schema/0002_shipping_rules.sql','worker/seeds/shipping-rules.sql',
)
def input_hash(root=ROOT):
    paths=sorted(set(FILES)|{str(p.relative_to(root)) for folder in ('worker/staging/migrations','worker/schema','worker/seeds') for p in (root/folder).rglob('*.sql')})
    h=hashlib.sha256()
    for name in paths:
        data=(root/name).read_bytes();h.update(name.encode()+b'\0'+str(len(data)).encode()+b'\0'+data)
    return h.hexdigest()

def commit_sha(root=ROOT):
    return subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
