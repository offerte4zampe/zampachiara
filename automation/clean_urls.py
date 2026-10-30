"""Build clean internal links; preserve merchant and affiliate URL bytes."""
import gzip
import json
import re
from html import escape, unescape
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qs

ROOT = Path(__file__).resolve().parents[1]


def product_url(offer):
    slug = offer.get('product_slug', '')
    if re.fullmatch(r'[a-z0-9][a-z0-9-]{1,200}', slug):
        return '/prodotto/' + slug
    return '/confronta-cibo'


def clean_url(value, offers=None, redirects=None):
    value = unescape(value)
    u = urlsplit(value)
    if u.scheme or u.netloc or not u.path:
        return value
    path = '/' + u.path.lstrip('/')
    if path in ('/prodotto.html', '/prodotto') and u.query:
        ids = parse_qs(u.query).get('id', [])
        if len(ids) == 1 and offers and ids[0] in offers:
            return product_url(offers[ids[0]]) + ('#' + u.fragment if u.fragment else '')
        # Unknown legacy IDs must keep their resolver, never guess a product.
        return value
    if path.endswith('/index.html'):
        path = path[:-10] or '/'
    elif path.endswith('.html') and not re.fullmatch(r'/google[\w-]+\.html', path):
        path = path[:-5]
    if redirects:
        path = redirects.get(path, path)
    return urlunsplit(('', '', path, u.query, u.fragment))


def apply(html, offers=None, redirects=None):
    return re.sub(r'\b(href|action)=("|\')(.*?)\2',
                  lambda m: m[1] + '=' + m[2] + escape(clean_url(m[3], offers, redirects), quote=True) + m[2], html)


def build():
    site = ROOT / 'site'
    catalog_path = site / 'data/catalog.json.gz'
    catalog = json.loads(gzip.decompress(catalog_path.read_bytes()))
    offers = {o['id']: o for o in catalog['offers']}
    for o in offers.values():
        o['product_url'] = product_url(o)
    catalog_path.write_bytes(gzip.compress(json.dumps(catalog, ensure_ascii=False, separators=(',', ':')).encode(), mtime=0))
    # Existing snapshots are adapted on deployment, without a new feed import.
    for name in ('home.json', 'search-index.json'):
        p = site / 'data' / name
        data = json.loads(p.read_text())
        for o in data.get('offers', []):
            source = offers.get(o.get('id'))
            if source:
                o['product_url'] = source['product_url']
                o['product_slug'] = source.get('product_slug', '')
        p.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n')
    redirects = {}
    for line in (site / '_redirects').read_text().splitlines():
        fields = line.split()
        if len(fields) == 3 and fields[2] == '301' and fields[1].startswith('/prodotto/'):
            redirects[fields[0].removesuffix('.html')] = fields[1]
    count = 0
    for p in site.rglob('*.html'):
        before = p.read_text()
        after = apply(before, offers, redirects)
        if after != before:
            p.write_text(after)
            count += 1
    print('Canonical internal links updated:', count)


if __name__ == '__main__':
    build()
