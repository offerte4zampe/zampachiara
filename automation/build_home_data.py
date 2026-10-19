"""Build a small home payload from the final catalog, without changing prices."""
import collections
import datetime
import gzip
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def build(catalog, now=None):
    now = now or datetime.datetime.now(datetime.timezone.utc)
    def recent(o):
        try:
            return 0 <= (now - datetime.datetime.fromisoformat(o['checked_at'].replace('Z', '+00:00'))).total_seconds() <= 36 * 3600
        except (ValueError, KeyError, TypeError):
            return False
    # Keep selection rules in home.js; at most 7 candidates per brand and source
    # are enough for its six distinct-brand picks and preferred-brand spotlight.
    rows = [o for o in catalog['offers'] if str(o.get('url','')).startswith('https://') and o.get('available') and isinstance(o.get('price'), (int, float)) and o['price'] > 0]
    sales = [o for o in rows if recent(o) and o.get('image') and isinstance(o.get('previous_price'), (int, float)) and o['previous_price'] > o['price'] and o['price'] / o['previous_price'] >= .4]
    sales.sort(key=lambda o: 1 - o['price']/o['previous_price'], reverse=True)
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
        if recent(o) and o.get('image') and o['price'] >= 15 and any(b in o.get('brand', '').lower() for b in ['royal canin', 'purina', 'trainer']) and isinstance(o.get('previous_price'), (int, float)) and o['previous_price'] > o['price'] and o['price'] / o['previous_price'] >= .4:
            add(o)
            break
    counts = collections.Counter(o['brand'] for o in rows if o.get('brand'))
    fields = ['id', 'title', 'merchant', 'merchant_id', 'brand', 'variant', 'price', 'previous_price', 'weight_kg', 'image', 'url', 'available', 'checked_at']
    return {k: catalog[k] for k in ['generated_at', 'refresh_hours', 'sources']} | {
        'stats': {'offers': len(catalog['offers']), 'brands': len({o.get('brand') for o in catalog['offers'] if o.get('brand')})},
        'top_brands': [brand for brand, count in counts.most_common(10)],
        'offers': [{k: o[k] for k in fields if k in o} for o in selected],
    }


def main():
    data = json.loads(gzip.decompress((ROOT/'site/data/catalog.json.gz').read_bytes()))
    path = ROOT/'site/data/home.json'
    payload = build(data)
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '\n')
    home = ROOT/'site/index.html'
    home.write_text(render_home(home.read_text(), payload))
    print(f'Home payload: {path.stat().st_size} bytes')



def pick(payload):
    """Same source diversity and distinct-brand order for HTML and hydration."""
    sales = sorted(payload['offers'], key=lambda o: -(1-o['price']/o['previous_price']))
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
    from html import escape as h
    from urllib.parse import urlencode
    import re
    def money(value):
        return f'{value:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')+' €'
    def link(label, **params):
        return f'<a href="confronta-cibo.html?{h(urlencode(params), quote=True)}">{h(label)}</a>'
    def card(o, spotlight=False):
        tag = 'h2' if spotlight else 'h3'
        image = o.get('image', '')
        img = f'<img src="{h(image,quote=True)}" alt="" width="160" height="145" loading="lazy">' if image.startswith('https://') else ''
        unit = f'<p class="micro">{money(o["price"]/o["weight_kg"])}/kg · spedizione esclusa</p>' if o.get('weight_kg') else '<p class="micro">Spedizione esclusa</p>'
        return f'''<article class="{'spotlight-product' if spotlight else 'home-deal'}" data-home-offer="{h(o['checked_at'],quote=True)}">{img}<p class="micro">{h(o['merchant'])} · {h(o['brand'])}</p><{tag}>{h(o['title'])}</{tag}><p class="micro">{h(o.get('variant') or '')}</p><p class="catalog-price"><strong>{money(o['price'])}</strong><del>{money(o['previous_price'])}</del><span class="catalog-sale">−{int((1-o['price']/o['previous_price'])*100+.5)}%</span></p>{unit}<p class="micro">Rilevato: <time datetime="{h(o['checked_at'],quote=True)}">{h(o['checked_at'][:16].replace('T',' '))} UTC</time></p>{link('Confronta il prodotto →', q=o['title'][:110]).replace('<a ', '<a class="btn secondary" ')}</article>'''
    deals, hero = pick(payload)
    parts = {
        'home-deals': ''.join(card(o) for o in deals),
        'home-spotlight': card(hero, True) if hero else link('Esplora il catalogo →'),
        'home-deals-status': 'Catalogo aggiornato il '+h(payload['generated_at'][:16].replace('T',' '))+' UTC. Prezzi rilevati, non in tempo reale. Selezione delle fonti disponibili, non una classifica dell’intero mercato.',
        'home-stats': ''.join('<span>'+h(s)+'</span>' for s in [f"{payload['stats']['offers']:,}".replace(',', '.')+' offerte importate', str(payload['stats']['brands'])+' marche', str(sum(s.get('offers',0)>0 for s in payload['sources']))+' negozi', 'Aggiornamenti ogni '+str(payload['refresh_hours'])+' ore']),
        'home-brands': ''.join(link(brand, brand=brand) for brand in payload['top_brands']),
        'home-shops': ''.join(link(s['name']+' · '+str(s['offers'])+' offerte →', shop=s['name']) for s in payload['sources'] if s.get('offers',0)>0),
    }
    for element_id, content in parts.items():
        html = replace_region(html, element_id, content)
    html = re.sub(r'(<main\b[^>]*?)(?: data-home-generated="[^"]*")?(>)', lambda m: re.sub(r' data-home-generated="[^"]*"', '', m[1])+' data-home-generated="'+h(payload['generated_at'],quote=True)+'"'+m[2], html, count=1)
    return html


if __name__ == '__main__':
    main()
