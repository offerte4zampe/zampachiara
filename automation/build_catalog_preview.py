"""Render a small, explicitly editorial fallback before the interactive catalog loads."""
import gzip
import json
from html import escape as h
from pathlib import Path
try:
    from automation.build_home_data import build, pick, replace_region
except ImportError:
    from build_home_data import build, pick, replace_region

ROOT = Path(__file__).resolve().parents[1]


def render_preview(html, catalog, now=None):
    payload = build(catalog, now=now)
    offers, _ = pick(payload)
    cards = []
    for o in offers:
        url = o.get('affiliate_url') or o['url']
        rel = 'sponsored noopener noreferrer' if o.get('affiliate_url') else 'noopener noreferrer'
        price = f"{o['price']:.2f}".replace('.', ',')
        unit = (f" · {o['price']/o['weight_kg']:.2f} €/kg".replace('.', ',')
                if o.get('weight_kg') else '')
        cards.append(f'<article class="catalog-card"><p class="micro">{h(o["merchant"])} · {h(o["brand"])}</p><h3><a class="product-title-link" href="{h(url, quote=True)}" rel="{rel}">{h(o["title"])}</a></h3><p>{h(o.get("variant") or "")}</p><p><strong>{price} €</strong>{unit} · spedizione esclusa</p><p class="micro">Rilevato: {h(o["checked_at"])} · disponibile al rilevamento</p></article>')
    content = '<h2>Dal catalogo dei negozi</h2><p>Selezione per nome e varietà di marche e fonti, non una classifica di convenienza. Prezzi rilevati, non in tempo reale. I link commerciali possono generare commissioni senza costi aggiuntivi per te.</p>'
    content += '<div class="catalog-grid">'+''.join(cards)+'</div>' if cards else '<p>Nessuna selezione recente disponibile. <a href="prodotti.html">Esplora le pagine prodotto</a>.</p>'
    html = replace_region(html, 'catalog-preview', content)
    return html


def main():
    catalog = json.loads(gzip.decompress((ROOT/'site/data/catalog.json.gz').read_bytes()))
    path = ROOT/'site/confronta-cibo.html'
    path.write_text(render_preview(path.read_text(), catalog))


if __name__ == '__main__':
    main()
