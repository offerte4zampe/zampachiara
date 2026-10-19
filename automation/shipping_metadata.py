"""Supplement the official feed with variant-specific shipping weights only."""
import datetime as dt
import json
from pathlib import Path

def supplement(rows, fetch_public, cachepath, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    path = Path(cachepath)
    try:
        cache = json.loads(path.read_text())
        age = (now-dt.datetime.fromisoformat(cache['checked_at'])).total_seconds()
    except (OSError, ValueError, KeyError):
        cache = {}; age = float('inf')
    if not 0 <= age < 86400:
        public, status = fetch_public()
        if status['status'] == 'ok' and public:
            cache = dict(checked_at=now.isoformat(),weights={o['id']:o['shipping_weight_kg'] for o in public if o.get('shipping_weight_kg',0) and o['shipping_weight_kg']>0})
            path.write_text(json.dumps(cache,separators=(',',':')))
            age = 0
    if not 0 <= age <= 7*86400:
        return
    for row in rows:
        weight = cache.get('weights',{}).get(row['id'])
        if isinstance(weight,(int,float)) and not isinstance(weight,bool) and 0<weight<=1000:
            row.update(shipping_weight_kg=weight,shipping_weight_checked_at=cache['checked_at'],shipping_weight_source='Bauzaar public variant grams')
