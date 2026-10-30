"""Remove the automatic AdSense loader until account/CMP/consent are verified.
Account discovery meta is removed until a certified CMP is active; affiliate destinations are retained.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
from urllib.parse import urlsplit
import re

ROOT = Path(__file__).resolve().parents[1]


class ScriptTag(HTMLParser):
    def __init__(self):
        super().__init__()
        self.src = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.src = dict(attrs).get('src', '')


def apply(html):
    def clean(match):
        parser = ScriptTag()
        parser.feed(match[0])
        try:
            url = urlsplit(parser.src)
            blocked = url.hostname == 'pagead2.googlesyndication.com' and url.path == '/pagead/js/adsbygoogle.js'
        except ValueError:
            blocked = False
        return '' if blocked else match[0]
    html=re.sub(r'<script\b[^>]*>.*?</script\s*>', clean, html, flags=re.S | re.I)
    html=re.sub(r'<meta\b(?=[^>]*\bname=[\"\']google-adsense-account[\"\'])[^>]*>','',html,flags=re.I)
    def anchor(m):
        tag=m[0];href=re.search(r'\bhref=([\"\'])(.*?)\1',tag,re.S);rel=re.search(r'\brel=([\"\'])(.*?)\1',tag,re.S)
        if not href:return tag
        url=urlsplit(unescape(href[2]));tokens=rel[2].split() if rel else []
        affiliate=url.path.startswith('/go/') and url.hostname in (None,'offerte4zampe.it') or 'sponsored' in tokens or url.hostname=='tc.tradetracker.net' or url.hostname in ('www.amazon.it','amazon.it') and 'tag=' in url.query
        if not affiliate:return tag
        tag=re.sub(r'\srel=([\"\'])(.*?)\1','',tag,flags=re.S)
        tag=re.sub(r'\starget=([\"\'])(.*?)\1','',tag,flags=re.S)
        values=['sponsored','nofollow','noopener','noreferrer']+[t for t in tokens if t not in ('sponsored','nofollow','noopener','noreferrer')]
        return tag[:-1]+' rel="'+' '.join(values)+'" target="_blank">'
    return re.sub(r'<a\b[^>]*>',anchor,html,flags=re.S)



def build():
    changed = 0
    for path in (ROOT / 'site').rglob('*.html'):
        before = path.read_text()
        after = apply(before)
        if after != before:
            path.write_text(after)
            changed += 1
    print('Automatic AdSense loaders removed:', changed)


if __name__ == '__main__':
    build()
