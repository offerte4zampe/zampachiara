"""Normalize the primary menu after all page generators, without touching offer links."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def apply(html):
    def menu(match):
        nav = match[0]
        nav = re.sub(r'<a\b(?=[^>]*\bclass="navcta")(?=[^>]*\bhref="confronta-cibo\.html")[^>]*>Cerca prodotti ↗</a>', '', nav)
        nav = re.sub(r'(<a\b[^>]*\bhref=")confronta-cibo\.html\?sale=1("[^>]*>)Offerte</a>', r'\1prodotti.html\2Prodotti</a>', nav)
        if not re.search(r'href="(?:/)?preferiti(?:\.html)?"', nav):
            nav=nav.replace('</nav>', '<a href="preferiti.html">Preferiti</a></nav>')
        if not re.search(r'href="(?:/)?codici-sconto(?:\.html)?"', nav):
            nav=nav.replace('</nav>', '<a href="/codici-sconto">Codici sconto</a></nav>')
        return nav
    html = html.replace('I link Bauzaar e Isola dei Tesori sono affiliati tramite TradeTracker:', 'I link Bauzaar, Isola dei Tesori e Paco Pet Shop sono affiliati tramite TradeTracker:')
    return re.sub(r'<nav\b(?=[^>]*\bid="navlinks")[^>]*>.*?</nav>', menu, html, flags=re.S)


def build():
    changed = 0
    for path in (ROOT / 'site').glob('*.html'):
        before = path.read_text()
        after = apply(before)
        if after != before:
            path.write_text(after)
            changed += 1
    print('Primary navigation updated:', changed)


if __name__ == '__main__':
    build()
