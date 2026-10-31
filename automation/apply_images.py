"""Image layout and fallback; local substitutions require a licensed manifest."""
import gzip
import json
import re
from html import escape, unescape
from pathlib import Path
from urllib.parse import urlsplit
ROOT = Path(__file__).resolve().parents[1]


def set_attr(tag, name, value):
    pattern = r'\s' + re.escape(name) + r'="[^"]*"'
    tag = re.sub(pattern, '', tag)
    return tag[:-1] + ' ' + name + '="' + escape(str(value), quote=True) + '">'


def apply(html, titles, manifest):
    def product_image(m):
        tag = m[0]
        src = re.search(r'\bsrc="([^"]*)"', tag)
        if not src:
            return tag
        remote = unescape(src[1])
        if remote not in titles and not remote.startswith('/img/p/'):
            return tag
        local = manifest.get(remote)
        if local and re.fullmatch(r'/img/p/[a-f0-9]{24}-400\.webp', local):
            tag = set_attr(tag, 'src', local)
        alt = re.search(r'\balt="([^"]*)"', tag)
        if not alt or not alt[1].strip():
            tag = set_attr(tag, 'alt', titles.get(remote, 'Immagine del prodotto'))
        for key, value in [('width',400), ('height',400), ('loading','lazy'), ('decoding','async')]:
            tag = set_attr(tag, key, value)
        return re.sub(r'\sfetchpriority="[^"]*"', '', tag)
    html = re.sub(r'<img\b[^>]*>', product_image, html)
    def article_label(match):
        article = match[0]
        if not re.search(r'<h[23]\b[^>]*>.*?<a\b[^>]*href=', article, re.S): return article
        return re.sub(r'<img\b[^>]*>', lambda m:set_attr(m[0], 'alt', ''), article)
    html = re.sub(r'<article\b[^>]*>.*?</article>', article_label, html, flags=re.S)
    # The main home offer is above the fold; prioritize only its image.
    def spotlight(match):
        return re.sub(r'<img\b[^>]*>', lambda m:set_attr(re.sub(r'\sloading="[^"]*"', '', m[0]), 'fetchpriority', 'high'), match[0], count=1)
    html = re.sub(r'<article\b[^>]*class="spotlight-product"[^>]*>.*?</article>', spotlight, html, flags=re.S)
    origins = sorted({urlsplit(unescape(src)).scheme+'://'+urlsplit(unescape(src)).netloc for src in re.findall(r'<img\b[^>]*src="([^"]+)"',html) if unescape(src) in titles and src.startswith('https://')})
    for origin in origins:
        link = '<link rel="preconnect" href="'+escape(origin,quote=True)+'">'
        if link not in html:
            html = html.replace('</head>',link+'</head>')
    script = '<script src="/assets/image-fallback.js" defer></script>'
    if script not in html and '<body' in html:
        html = html.replace('</body>',script+'</body>')
    return html


def main():
    site = ROOT/'site'
    catalog = json.loads(gzip.decompress((site/'data/catalog.json.gz').read_bytes()))
    titles = {o['image']: o.get('canonical_title') or o['title'] for o in catalog['offers'] if o.get('image')}
    path = site/'data/product-images.json'
    raw = json.loads(path.read_text()) if path.exists() else {'images': {}}
    try:
        from .cache_product_images import permitted
    except ImportError:
        from cache_product_images import permitted
    rules = json.loads((ROOT/'automation/image-rights.json').read_text())['stores']
    licensed = {o.get('image') for o in catalog['offers'] if permitted(rules.get(o.get('merchant_id'), {}))}
    manifest = {remote: local for remote, local in raw['images'].items() if remote in licensed and re.fullmatch(r'/img/p/[a-f0-9]{24}-400\.webp', local) and (site/local.lstrip('/')).is_file()}
    for p in site.rglob('*.html'):
        before = p.read_text()
        after = apply(before, titles, manifest)
        if before != after:
            p.write_text(after)
    print('Product image markup updated; licensed local images:',len(manifest))


if __name__ == '__main__':
    main()
