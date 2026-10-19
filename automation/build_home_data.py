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
    rows = [o for o in catalog['offers'] if o.get('available') and isinstance(o.get('price'), (int, float)) and o['price'] > 0]
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
    path.write_text(json.dumps(build(data), ensure_ascii=False, separators=(',', ':')) + '\n')
    print(f'Home payload: {path.stat().st_size} bytes')


if __name__ == '__main__':
    main()
