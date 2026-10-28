"""Apply explicitly reviewed offer equivalences; no title similarity matching."""
import datetime as dt


def apply(offers, reviews, now):
    # A previous review must be revalidated against today's exact records.
    for o in offers:
        if str(o.get('gtin_source', '')).startswith('reviewed:'):
            o['gtin'] = ''
            o['gtin_source'] = ''
            for key in ('identity_review', 'identity_evidence', 'identity_expires_at'):
                o.pop(key, None)
    by_id = {o['id']: o for o in offers}
    applied = 0
    for review in reviews:
        try:
            start = dt.datetime.fromisoformat(review['reviewed_at'])
            end = dt.datetime.fromisoformat(review['expires_at'])
            if start.tzinfo is None or end.tzinfo is None or not start <= now <= end:
                continue
            members = [(by_id.get(member['id']), member) for member in review['offers']]
            if len(members) < 2 or any(not o or any(o.get(k) != spec[k] for k in ('title', 'url', 'brand')) or o.get('weight_kg') != review['weight_kg'] or o.get('quantity_verified') is False for o, spec in members):
                continue
            reference = by_id[review['reference_id']]
            code = reference.get('gtin', '')
            # The reference must retain its merchant-provided identifier.
            if not isinstance(code, str) or len(code) not in (8,12,13,14) or not code.isascii() or not code.isdigit() or len(set(code)) == 1:
                continue
            check = (10-sum(int(n)*(3 if i%2==0 else 1) for i,n in enumerate(reversed(code[:-1])))%10)%10
            if check != int(code[-1]):
                continue
            if code.zfill(14) != str(review['gtin']).zfill(14) or reference.get('gtin_source', '').startswith('reviewed:'):
                continue
            if any(o.get('gtin') and o['gtin'].zfill(14) != code.zfill(14) for o, _ in members):
                continue
            for o, _ in members:
                if not o.get('gtin'):
                    o.update(gtin=code, gtin_source='reviewed:'+review['id'], identity_review=review['id'], identity_evidence=review['evidence'], identity_expires_at=review['expires_at'])
                    applied += 1
        except (KeyError, TypeError, ValueError):
            continue
    return applied
