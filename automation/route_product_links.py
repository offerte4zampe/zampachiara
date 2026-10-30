"""Route catalog product links through the internal comparison before merchant choice."""
import gzip
import json
import re
from html import escape, unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlencode, quote

try:
    from .product_link import product_url
except ImportError:
    from product_link import product_url

ROOT = Path(__file__).resolve().parents[1]


class Anchor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.attrs = {}
        self.label = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.attrs = dict(attrs)

    def handle_data(self, data):
        self.label.append(data)


def apply(html, offers, merchant_choice=False):
    byurl = {}
    for o in offers:
        for url in (o.get('url'), o.get('affiliate_url')):
            if url:
                byurl.setdefault(url, {})[o['id']] = o

    def route(match):
        parser = Anchor()
        parser.feed(match[0])
        attrs = parser.attrs
        rows = list(byurl.get(attrs.get('href'), {}).values())
        if not rows:
            return match[0]
        title_link = 'product-title-link' in attrs.get('class', '').split()
        outbound = merchant_choice and not title_link
        label = ''.join(parser.label).strip()
        exact = [o for o in rows if label == o.get('title') or label == o.get('title', '')+' — '+o.get('variant', '')]
        if len(rows) > 1 and len(exact) == 1:
            rows = exact
        if len(rows) != 1:
            # Never select a different format when the catalog URL is ambiguous.
            return '<span>'+match[0].split('>', 1)[1].rsplit('</a', 1)[0]+'</span>'
        attrs['href'] = ('/go/'+quote(rows[0]['id'],safe='')+'?from=product') if outbound else product_url(rows[0])
        for key in ('rel', 'target', 'data-metric', 'data-merchant'):
            attrs.pop(key, None)
        if outbound: attrs['rel'] = 'sponsored nofollow noopener noreferrer'
        opening = '<a '+ ' '.join(escape(k)+'="'+escape(v or '', quote=True)+'"' for k,v in attrs.items())+'>'
        inner = match[0].split('>', 1)[1].rsplit('</a', 1)[0]
        if not outbound and label in ('Vai al negozio ↗', 'Vedi nel negozio ↗'):
            inner = 'Vedi offerta →' if rows[0].get('canonical_shop_count', 2) < 2 else 'Confronta nei negozi →'
        return opening+inner+'</a>'
    # Existing legacy links need normalization too, not just external merchant URLs.
    byid={o['id']:o for o in offers}
    from urllib.parse import parse_qs, urlsplit
    def legacy(m):
        u=urlsplit(unescape(m[1]))
        if u.netloc or u.path not in ('prodotto.html','/prodotto.html','/prodotto'):return m[0]
        ids=parse_qs(u.query).get('id',[])
        if len(ids)!=1 or ids[0] not in byid:return m[0]
        return 'href="'+escape(product_url(byid[ids[0]]),quote=True)+'"'
    html=re.sub(r'href="([^"]+)"',legacy,html)
    return re.sub(r'<a\b[^>]*>.*?</a\s*>', route, html, flags=re.S | re.I)


def build():
    offers = json.loads(gzip.decompress((ROOT/'site/data/catalog.json.gz').read_bytes()))['offers']
    changed = 0
    for path in (ROOT/'site').glob('*.html'):
        before = path.read_text()
        after = apply(before, offers, merchant_choice=path.stem.startswith('prezzi-'))
        if before != after:
            path.write_text(after)
            changed += 1
    print('Internal product navigation updated:', changed)


if __name__ == '__main__':
    build()
