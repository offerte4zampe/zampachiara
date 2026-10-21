"""Remove the automatic AdSense loader until account/CMP/consent are verified.
Ownership meta tags and approved affiliate links are retained.
"""
from pathlib import Path
from html.parser import HTMLParser
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
    return re.sub(r'<script\b[^>]*>.*?</script\s*>', clean, html, flags=re.S | re.I)


def build():
    changed = 0
    for path in (ROOT / 'site').glob('*.html'):
        before = path.read_text()
        after = apply(before)
        if after != before:
            path.write_text(after)
            changed += 1
    print('Automatic AdSense loaders removed:', changed)


if __name__ == '__main__':
    build()
