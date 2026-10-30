"""Include shared HTML partials after page generation and before asset deployment.

Only site chrome, internal-link labels and affiliate disclosure copy are changed.
Offer destinations, tracking preferences and shipping data are left intact.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
PARTIALS = ROOT / 'automation' / 'partials'


def affiliate_names(network='TradeTracker'):
    stores = json.loads((ROOT / 'automation/stores.json').read_text())
    names = [s['name'] for s in stores if s['affiliate'] and s['network'] == network]
    return ', '.join(names[:-1]) + ' e ' + names[-1] if len(names) > 1 else ''.join(names)


def disclosure():
    return f'I link {affiliate_names()} sono affiliati tramite TradeTracker: possiamo ricevere una commissione senza costi aggiuntivi per te.'


def apply(html):
    # Preserve the current-page indication while using identical links everywhere.
    current = re.search(r'<nav\b[^>]*id="navlinks"[^>]*>(.*?)</nav>', html, re.S)
    active = None
    if current:
        for tag in re.findall(r'<a\b[^>]*>', current[1]):
            if 'aria-current="page"' in tag:
                match = re.search(r'href="([^"]+)"', tag)
                if match:
                    active = '/' + match[1].removesuffix('.html').lstrip('/')
                    if active == '/index':
                        active = '/'
    header = (PARTIALS / 'header.html').read_text().strip()
    if active:
        header = header.replace(f'href="{active}"', f'href="{active}" aria-current="page"')
    nav = re.search(r'<nav\b[^>]*id="navlinks"[^>]*>.*?</nav>', header, re.S)[0]
    html = re.sub(r'<nav\b[^>]*id="navlinks"[^>]*>.*?</nav>', lambda _: nav, html, count=1, flags=re.S)
    footer = (PARTIALS / 'footer.html').read_text().strip().replace('{{affiliate_disclosure}}', disclosure())
    html = re.sub(r'<header\b[^>]*>.*?</header>', lambda _: header, html, count=1, flags=re.S)
    html = re.sub(r'<footer\b[^>]*>.*?</footer>', lambda _: footer, html, count=1, flags=re.S)
    # These are factual lists of the currently connected affiliate merchants.
    names = affiliate_names()
    html = re.sub(r'Trasparenza: nel catalogo i link verso .*?Le commissioni non determinano l’ordinamento dei risultati\.',
                  lambda _: 'Trasparenza: ' + disclosure() + ' Le commissioni non determinano l’ordinamento dei risultati.', html)
    for pattern, replacement in (
        (r'I link [^<>.]+ utilizzano il tracciamento di TradeTracker', f'I link {names} utilizzano il tracciamento di TradeTracker'),
        (r'Importiamo i feed ufficiali [^<>.]+ tramite TradeTracker', f'Importiamo i feed ufficiali {names} tramite TradeTracker'),
        (r'I collegamenti [^<>.]+ sono affiliati tramite TradeTracker', f'I collegamenti {names} sono affiliati tramite TradeTracker'),
    ):
        html = re.sub(pattern, lambda _: replacement, html)
    html = re.sub(r'I link [^<>.]+ sono affiliati tramite TradeTracker: possiamo ricevere una commissione senza costi aggiuntivi per te\.', lambda _: disclosure(), html)
    # Keep the historical date, but distinguish it from the current partners.
    html = html.replace('Dal 19 ottobre 2026 è attiva la collaborazione affiliata con Bauzaar tramite TradeTracker.',
                        'Dal 19 ottobre 2026 è attiva la prima collaborazione affiliata. ' + disclosure())
    html = re.sub(r'(<a\b[^>]*href="(?!https?:|//|mailto:|tel:)[^"]*"[^>]*>[^<]*) ↗(</a>)', r'\1\2', html)
    return html


def build():
    changed = 0
    for path in (ROOT / 'site').rglob('*.html'):
        before = path.read_text()
        after = apply(before)
        if after != before:
            path.write_text(after)
            changed += 1
    print('Shared header, footer and disclosure updated:', changed)


if __name__ == '__main__':
    build()
