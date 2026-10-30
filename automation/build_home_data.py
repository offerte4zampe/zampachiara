"""Build a small home payload from the final catalog, without changing prices."""
import collections
import datetime
import gzip
import json
import pathlib
import re


try:
    from automation.report_link import error_link
    from automation.product_link import product_url
except ImportError:
    from report_link import error_link
    from product_link import product_url

ROOT = pathlib.Path(__file__).resolve().parents[1]


def build(catalog, now=None):
    now = now or datetime.datetime.now(datetime.timezone.utc)
    counts_by_store = collections.Counter(o.get('merchant_id') for o in catalog['offers'])
    catalog = {**catalog, 'sources': [{**s, 'offers': counts_by_store[s['id']]} for s in catalog['sources']]}
    def recent(o):
        try:
            return 0 <= (now - datetime.datetime.fromisoformat(o['checked_at'].replace('Z', '+00:00'))).total_seconds() <= 12 * 3600
        except (ValueError, KeyError, TypeError):
            return False
    # Current prices, independent of unverified comparison prices or commissions.
    def home_topic(o):
        title = o.get('title', '')
        if len(title) > 180 or re.search(r'\b(ricambi?o?|elastici)\b', title, re.I):
            return False
        label = title+' '+o.get('category', '')
        return bool(re.search(r'\b(cani|gatti|cane|gatto|dog|cat|crocchette|umido|food|tiragraffi|lettiera)\b', label, re.I)) and not re.search(r'integrator|veterinar|diabet|renal|medicat|diete vet|calmant|antiansia|antiparassitar|feromon|farmac', label, re.I)
    rows = [o for o in catalog['offers'] if str(o.get('url','')).startswith('https://') and o.get('available') and isinstance(o.get('price'), (int, float)) and o['price'] > 0 and home_topic(o)]
    sales = sorted((o for o in rows if recent(o) and o.get('image')), key=lambda o: (o['title'].casefold(), o['id']))
    selected = []
    seen = set()
    def add(o):
        if o['id'] not in seen:
            selected.append(o)
            seen.add(o['id'])
    for source in catalog.get('sources', []):
        brands = set()
        for o in sales:
            if o['merchant_id'] == source['id'] and o.get('brand') not in brands:
                add(o)
                brands.add(o.get('brand'))
                if len(brands) == 7:
                    break
    for o in rows:
        if recent(o) and o.get('image') and o['price'] >= 15 and any(b in o.get('brand', '').lower() for b in ['royal canin', 'purina', 'trainer']):
            add(o)
            break
    counts = collections.Counter(o['brand'] for o in rows if o.get('brand'))
    fields = ['id', 'title', 'merchant', 'merchant_id', 'brand', 'variant', 'price', 'weight_kg', 'image', 'url', 'affiliate_url', 'available', 'checked_at', 'canonical_title', 'canonical_format', 'canonical_shop_count', 'product_slug', 'product_url', 'unit_price', 'unit_price_unit']
    return {k: catalog[k] for k in ['generated_at', 'refresh_hours', 'sources']} | {
        'stats': {'offers': len(catalog['offers']), 'brands': len({o.get('brand') for o in catalog['offers'] if o.get('brand')})},
        'top_brands': [brand for brand, count in counts.most_common(10)],
        'offers': [{k: o[k] for k in fields if k in o} for o in selected],
    }



def search_index(catalog):
    """Only names and provenance for suggestions: no prices, images or tracking URLs."""
    fields = ('id', 'title', 'variant', 'brand', 'gtin', 'merchant', 'available', 'checked_at', 'product_slug', 'product_url')
    return {'generated_at': catalog.get('generated_at'), 'offers': [
        {key: offer[key] for key in fields if key in offer}
        for offer in catalog.get('offers', []) if isinstance(offer.get('title'), str)
    ]}


def main():
    data = json.loads(gzip.decompress((ROOT/'site/data/catalog.json.gz').read_bytes()))
    path = ROOT/'site/data/home.json'
    index = ROOT/'site/data/search-index.json'
    index.write_text(json.dumps(search_index(data), ensure_ascii=False, separators=(',', ':'))+'\n')
    print(f'Search index: {index.stat().st_size} bytes; gzip {len(gzip.compress(index.read_bytes()))} bytes')
    payload = build(data)
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '\n')
    home = ROOT/'site/index.html'
    home.write_text(render_home(home.read_text(), payload))
    print(f'Home payload: {path.stat().st_size} bytes')



def pick(payload):
    """Same source diversity and distinct-brand order for HTML and hydration."""
    sales = payload['offers']
    picked, brands = [], set()
    for source in payload['sources']:
        found = next((o for o in sales if o['merchant_id'] == source['id'] and o['brand'] not in brands), None)
        if found:
            picked.append(found)
            brands.add(found['brand'])
    for o in sales:
        if len(picked) >= 6:
            break
        if o['brand'] not in brands:
            picked.append(o)
            brands.add(o['brand'])
    hero = next((o for o in payload['offers'] if o['price'] >= 15 and any(b in o['brand'].lower() for b in ['royal canin', 'purina', 'trainer'])), None)
    return picked, hero or (picked[0] if picked else None)


def replace_region(html, element_id, content):
    import re
    opening = re.search(r'<(div|p)\b[^>]*\bid="'+re.escape(element_id)+r'"[^>]*>', html)
    if not opening:
        raise ValueError('Missing home region: '+element_id)
    depth = 1
    for token in re.finditer(r'</?'+opening[1]+r'\b[^>]*>', html[opening.end():]):
        depth += -1 if token[0].startswith('</') else 1
        if not depth:
            end = opening.end()+token.start()
            return html[:opening.end()]+content+html[end:]
    raise ValueError('Unclosed home region: '+element_id)


def render_home(html, payload):
    from html import escape as h, unescape
    from urllib.parse import urlencode
    import re
    def money(value):
        return f'{value:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')+' €'
    region = re.search(r'<div\b[^>]*\bid="home-brands"[^>]*>', html)
    mapping = re.search(r'data-brand-pages="([^"]*)"', region[0]) if region else None
    try:
        brand_pages = json.loads(unescape(mapping[1])) if mapping else {}
    except (ValueError, TypeError):
        brand_pages = {}
    def link(label, **params):
        target = brand_pages.get(params.get('brand'))
        if isinstance(target, str) and re.fullmatch(r'/marca-[a-z0-9-]+', target):
            return f'<a href="{h(target, quote=True)}">{h(label)}</a>'
        return f'<a href="confronta-cibo.html?{h(urlencode(params), quote=True)}">{h(label)}</a>'
    def card(o, spotlight=False):
        tag = 'h2' if spotlight else 'h3'
        image = o.get('image', '')
        img = f'<img src="{h(image,quote=True)}" alt="" width="160" height="145" loading="lazy">' if image.startswith('https://') else ''
        unit = f'<p class="micro">{money(o["price"]/o["weight_kg"])}/kg · spedizione esclusa</p>' if o.get('weight_kg') else '<p class="micro">Spedizione esclusa</p>'
        title = o.get('canonical_title') or o['title']
        cta = 'Vedi offerta →' if o.get('canonical_shop_count', 2) < 2 else 'Confronta nei negozi →'
        if o.get('unit_price') and o.get('unit_price_unit'):
            unit = '<p class="micro">'+money(o['unit_price'])+'/'+h(o['unit_price_unit'])+' · spedizione esclusa</p>'
        return f'''<article class="{'spotlight-product' if spotlight else 'home-deal'}" data-home-offer="{h(o['checked_at'],quote=True)}">{img}<p class="micro">{h(o['merchant'])} · {h(o['brand'])}</p><{tag}><a class="product-title-link" href="{h(product_url(o),quote=True)}">{h(title)}</a></{tag}><p class="micro">{h(o.get('variant') or '')}</p><p class="catalog-price"><strong>{money(o['price'])}</strong></p>{unit}<p class="micro">Rilevato: <time datetime="{h(o['checked_at'],quote=True)}">{h(o['checked_at'][:16].replace('T',' '))} UTC</time></p><a class="btn secondary" href="{h(product_url(o),quote=True)}">{cta}</a>{error_link(o)}</article>'''
    deals, hero = pick(payload)
    parts = {
        'home-deals': ''.join(card(o) for o in deals),
        'home-spotlight': card(hero, True) if hero else link('Esplora il catalogo →'),
        'home-deals-status': 'Catalogo aggiornato il '+h(payload['generated_at'][:16].replace('T',' '))+' UTC. Prezzi rilevati, non in tempo reale. Selezione delle fonti disponibili, non una classifica dell’intero mercato.',
        'home-stats': ''.join('<span>'+h(s)+'</span>' for s in [f"{payload['stats']['offers']:,}".replace(',', '.')+' offerte importate', str(payload['stats']['brands'])+' marche', str(sum(s.get('offers',0)>0 for s in payload['sources']))+' negozi', 'Verifiche programmate ogni '+str(payload['refresh_hours'])+' ore']),
        'home-brands': ''.join(link(brand, brand=brand) for brand in payload['top_brands']),
        'home-shops': ''.join(link(s['name']+' · '+str(s['offers'])+' offerte →', shop=s['name']) for s in payload['sources'] if s.get('offers',0)>0),
    }
    for element_id, content in parts.items():
        html = replace_region(html, element_id, content)
    # Keep both SEO descriptions aligned with the actual imported shops, not a stale static list.
    shops = [s['name'] for s in payload['sources'] if s.get('offers', 0) > 0 and s.get('name')]
    if shops:
        shop_names = ', '.join(shops[:-1]) + (' e ' if len(shops) > 1 else '') + shops[-1]
        summary = f'Confronta offerte e prezzi per cani e gatti da {shop_names}. Prezzi rilevati, non in tempo reale.'
        html = re.sub(r'(<meta\s+(?:name="description"|property="og:description")\s+content=")[^"]*(">)',
                      lambda m: m[1] + h(summary, quote=True) + m[2], html)
    html = re.sub(r'(<main\b[^>]*?)(?: data-home-generated="[^"]*")?(>)', lambda m: re.sub(r' data-home-generated="[^"]*"', '', m[1])+' data-home-generated="'+h(payload['generated_at'],quote=True)+'"'+m[2], html, count=1)
    return html


if __name__ == '__main__':
    main()
