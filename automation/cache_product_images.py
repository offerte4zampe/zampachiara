"""Cache only explicitly licensed product images; no inferred permissions."""
import gzip
import hashlib
import io
import json
from pathlib import Path
from urllib.parse import urlsplit
import urllib.request
ROOT = Path(__file__).resolve().parents[1]


try:
    from .image_policy import permitted, eligible
except ImportError:
    from image_policy import permitted, eligible
import concurrent.futures


def allowed_url(url, hosts):
    try:
        u = urlsplit(url)
        return u.scheme == 'https' and u.hostname in hosts and u.port in (None, 443) and not u.username and not u.password
    except ValueError:
        return False


def download(url, hosts):
    if not allowed_url(url, hosts):
        raise ValueError('Image host not allowlisted')
    class Redirects(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            if not allowed_url(newurl, hosts):
                raise ValueError('Image redirect host not allowlisted')
            return super().redirect_request(req, fp, code, msg, headers, newurl)
    req = urllib.request.Request(url, headers={'User-Agent': 'Offerte4ZampeImages/1.0'})
    with urllib.request.build_opener(Redirects()).open(req, timeout=20) as response:
        data = response.read(10_000_001)
    if len(data) > 10_000_000:
        raise ValueError('Image too large')
    return data


def convert(data, target):
    from PIL import Image, ImageOps
    with Image.open(io.BytesIO(data)) as image:
        if image.width * image.height > 40_000_000:
            raise ValueError('Image dimensions too large')
        image = ImageOps.exif_transpose(image).convert('RGBA')
        image.thumbnail((400, 400), Image.Resampling.LANCZOS)
        square = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
        square.alpha_composite(image, ((400-image.width)//2, (400-image.height)//2))
        target.parent.mkdir(parents=True, exist_ok=True)
        square.save(target, 'WEBP', quality=82, method=6)


def cache(offers, rules, site, fetch=download, limit=500, priority_ids=()):
    manifest, report = {}, {'cached': 0, 'unlicensed': 0, 'failed': 0, 'limited': 0}
    priority=set(priority_ids)
    rows=sorted(offers,key=lambda o:(o.get('id') not in priority,-int(o.get('canonical_shop_count') or 0),not o.get('available'),o['id']))
    jobs={}
    for offer in rows:
        rule=rules.get(offer.get('merchant_id'),{})
        if not eligible(offer,rule):
            report['unlicensed']+=1
            continue
        remote=offer.get('image')
        if not remote or not allowed_url(remote,rule.get('hosts',[])):continue
        # Same upstream file is stored once, regardless of how many offers use it.
        path=site/'img/p'/(hashlib.sha256(remote.encode()).hexdigest()[:24]+'-400.webp')
        if path.is_file():manifest[remote]='/img/p/'+path.name
        elif remote not in jobs:
            if len(jobs)>=limit:report['limited']+=1
            else:jobs[remote]=(path,rule.get('hosts',[]))
    def save(item):
        remote,(path,hosts)=item
        try:
            convert(fetch(remote,hosts),path)
            return remote,'/img/p/'+path.name
        except Exception:return remote,None
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for remote,local in pool.map(save,jobs.items()):
            if local:manifest[remote]=local;report['cached']+=1
            else:report['failed']+=1
    return manifest,report


def main():
    catalog = json.loads(gzip.decompress((ROOT/'site/data/catalog.json.gz').read_bytes()))
    rules = json.loads((ROOT/'automation/image-rights.json').read_text())['stores']
    home_path=ROOT/'site/data/home.json'
    home=json.loads(home_path.read_text()) if home_path.exists() else {}
    manifest, report = cache(catalog['offers'], rules, ROOT/'site', priority_ids=[o['id'] for o in home.get('offers',[])])
    for o in catalog['offers']:
        o.pop('image_local', None)
        if o.get('image') in manifest:
            o['image_local'] = manifest[o['image']]
    (ROOT/'site/data/catalog.json.gz').write_bytes(gzip.compress(json.dumps(catalog, ensure_ascii=False, separators=(',', ':')).encode(), mtime=0))
    for path in (ROOT/'site/data/canonical-products').glob('*.json'):
        products = json.loads(path.read_text())
        for product in products.values():
            product.pop('image_local', None)
            if product.get('image') in manifest:
                product['image_local'] = manifest[product['image']]
            for offer in product.get('offers', []):
                offer.pop('image_local', None)
                if offer.get('image') in manifest:
                    offer['image_local'] = manifest[offer['image']]
        path.write_text(json.dumps(products, ensure_ascii=False, separators=(',', ':'))+'\n')
    sources={o['image']:{'offer_id':o['id'],'merchant_id':o['merchant_id'],'source':o.get('image_source'),'evidence':rules[o['merchant_id']]['evidence']} for o in catalog['offers'] if o.get('image') in manifest and eligible(o,rules.get(o.get('merchant_id'),{}))}
    (ROOT/'site/data/product-images.json').write_text(json.dumps({'images': manifest, 'sources':sources, 'report': report}, separators=(',', ':'))+'\n')
    print('Product image cache:', report)


if __name__ == '__main__':
    main()
