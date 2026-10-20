"""Keep social previews complete after every static-page generation."""
from html import escape
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://offerte4zampe.it/assets/'


def apply(html, slug):
    if 'content="noindex,follow"' in html:
        return html
    image = 'social-compare.png' if slug.startswith(('prezzi-', 'crocchette-', 'lettiere-')) or slug in ['confronta-cibo','prodotti','confronti-prodotti'] else 'social-home.png'
    if '"@type":"Article"' in html or '"@type": "Article"' in html:
        image = 'social-guide.png'
    html = re.sub(r'<meta\b[^>]*(?:property|name)="(?:og:image(?::\w+)?|twitter:card|twitter:image(?::\w+)?)"[^>]*>','',html)
    tags = f'<meta property="og:image" content="{BASE+image}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:type" content="image/png"><meta property="og:image:alt" content="Offerte a 4 Zampe: prezzi e offerte per cani e gatti"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{BASE+image}">'
    return html.replace('</head>',tags+'</head>')


def build():
    changed = 0
    for path in (ROOT/'site').glob('*.html'):
        before = path.read_text()
        if '<head>' not in before and '<head ' not in before:
            continue
        after = apply(before,path.stem)
        if before != after:
            path.write_text(after)
            changed += 1
    print('Social metadata updated:',changed)


if __name__ == '__main__':
    build()
