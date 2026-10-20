"""Conservative validation before publishing; outliers are suspicions, not proven errors."""
import copy
import datetime
import gzip
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit

try:
    from .build_matched_pages import valid_gtin
except ImportError:
    from build_matched_pages import valid_gtin

ROOT = Path(__file__).resolve().parents[1]


def positive(value):
    return isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value) and value > 0


def check(catalog, now):
    output = copy.deepcopy(catalog)
    accepted, quarantined, repaired = [], [], []
    counts = Counter(o.get('id') for o in output['offers'])

    def record(o, reasons):
        return {**{k: o.get(k) for k in ('id', 'title', 'variant', 'merchant', 'merchant_id', 'checked_at')}, 'reasons': reasons}

    for o in output['offers']:
        reasons = []
        if not o.get('id') or counts[o.get('id')] > 1:
            reasons.append('missing_or_duplicate_id')
        if not positive(o.get('price')):
            reasons.append('invalid_price')
        try:
            url = urlsplit(o.get('url') or '')
            if url.scheme != 'https' or not url.hostname or url.username or url.password:
                reasons.append('invalid_merchant_url')
        except ValueError:
            reasons.append('invalid_merchant_url')
        try:
            stamp = datetime.datetime.fromisoformat(o['checked_at'].replace('Z', '+00:00'))
            if stamp.tzinfo is None or not -300 <= (now-stamp).total_seconds() <= 36*3600:
                reasons.append('stale_or_future_observation')
        except (KeyError, TypeError, ValueError):
            reasons.append('invalid_observation_date')
        if reasons:
            quarantined.append(record(o, reasons))
            continue
        for field in ('weight_kg', 'shipping_weight_kg'):
            if o.get(field) is not None and not positive(o[field]):
                o[field] = None
                repaired.append(record(o, ['invalid_'+field+'_removed']))
        accepted.append(o)

    # Use independent merchants, exact checksum-valid GTIN/brand/net weight only.
    # Two agreeing peers are required; broad category medians are never used.
    groups = defaultdict(list)
    for o in accepted:
        if valid_gtin(o.get('gtin')) and positive(o.get('weight_kg')) and o.get('brand', '').strip() and o.get('available'):
            groups[(o['gtin'].zfill(14), o['brand'].strip().casefold(), o['weight_kg'])].append(o)
    suspects = set()
    for rows in groups.values():
        for o in rows:
            peers = defaultdict(list)
            for other in rows:
                if other['merchant_id'] != o['merchant_id']:
                    peers[other['merchant_id']].append(other['price'])
            values = [statistics.median(prices) for prices in peers.values()]
            if len(values) < 2 or max(values)/min(values) > 1.2:
                continue
            baseline = statistics.median(values)
            if o['price'] < baseline*.5 or o['price'] > baseline*1.5:
                suspects.add(o['id'])
    for o in accepted:
        if o['id'] in suspects:
            quarantined.append(record(o, ['exact_product_peer_outlier_pending_review']))
    output['offers'] = [o for o in accepted if o['id'] not in suspects]
    report = {'checked_at': now.isoformat(), 'input_offers': len(catalog['offers']), 'published_offers': len(output['offers']),
              'quarantined': quarantined, 'repaired': repaired,
              'method': 'Validazione sintattica e temporale. Anomalie oltre ±50% solo con GTIN, marca e peso netto identici e almeno due altri negozi concordanti entro il 20%. Una sospensione non prova un errore del negozio; nessuna modifica dei prezzi.'}
    return output, report


def build():
    path = ROOT/'site/data/catalog.json.gz'
    catalog = json.loads(gzip.decompress(path.read_bytes()))
    catalog, report = check(catalog, datetime.datetime.now(datetime.timezone.utc))
    path.write_bytes(gzip.compress(json.dumps(catalog, ensure_ascii=False, separators=(',', ':')).encode(), mtime=0))
    (ROOT/'site/data/catalog-quarantine.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    quality_path = ROOT/'site/data/catalog-quality.json'
    quality = json.loads(quality_path.read_text())
    groups = defaultdict(set)
    for o in catalog['offers']:
        if o.get('gtin') and positive(o.get('weight_kg')):
            groups[(o['gtin'].zfill(14), o['brand'].strip().casefold(), o['weight_kg'])].add(o['merchant_id'])
    quality.update(offers=len(catalog['offers']), with_valid_gtin=sum(valid_gtin(o.get('gtin')) for o in catalog['offers']),
                   cross_shop_groups=sum(len(shops)>1 for shops in groups.values()), quarantined=len(report['quarantined']), repaired=len(report['repaired']))
    quality_path.write_text(json.dumps(quality, ensure_ascii=False))
    print(json.dumps({k: report[k] for k in ('input_offers', 'published_offers')}))


if __name__ == '__main__':
    build()
