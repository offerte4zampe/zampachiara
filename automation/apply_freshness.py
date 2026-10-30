"""Refresh lightweight HTML and source-age metadata before deploying the snapshot."""
import datetime as dt
import gzip
import json
from pathlib import Path
try:
    from .freshness import source_freshness, banner
    from .build_home_data import build, render_home
    from .build_catalog_preview import render_preview
except ImportError:
    from freshness import source_freshness, banner
    from build_home_data import build, render_home
    from build_catalog_preview import render_preview
ROOT = Path(__file__).resolve().parents[1]


def main():
    now = dt.datetime.now(dt.timezone.utc)
    p = ROOT / 'site/data/catalog.json.gz'
    catalog = json.loads(gzip.decompress(p.read_bytes()))
    from collections import Counter
    counts = Counter(o.get('merchant_id') for o in catalog['offers'])
    catalog['sources'] = [source_freshness({**s, 'offers': counts[s['id']]}, catalog['offers'], now) for s in catalog['sources']]
    p.write_bytes(gzip.compress(json.dumps(catalog, ensure_ascii=False, separators=(',', ':')).encode(), mtime=0))
    home = build(catalog, now)
    (ROOT / 'site/data/home.json').write_text(json.dumps(home, ensure_ascii=False, separators=(',', ':')) + '\n')
    page = ROOT / 'site/index.html'
    page.write_text(render_home(page.read_text(), home))
    page = ROOT / 'site/confronta-cibo.html'
    page.write_text(banner(render_preview(page.read_text(), catalog, now), catalog['sources'], now))
    print('Freshness checked for', len(catalog['sources']), 'stores; home threshold: 12 hours')


if __name__ == '__main__':
    main()
