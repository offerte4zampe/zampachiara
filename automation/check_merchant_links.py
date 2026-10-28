"""Bounded HEAD checks of direct product URLs, never affiliate redirects or cookies."""
import datetime as dt
import gzip
import json
import re
import time
import urllib.error
import urllib.request
import urllib.robotparser
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
UA = 'Offerte4Zampe-LinkCheck/1.0 (+https://offerte4zampe.it/contatti)'
HOSTS = {'bauzaar': 'www.bauzaar.it', 'webpet': 'www.webpet.it',
         'animaliapet': 'www.animaliapet.eu', 'isola-dei-tesori': 'www.isoladeitesori.it', 'paco': 'www.pacopetshop.it'}


def safe_product(offer):
    """Only existing direct catalog URLs, with exact variant query where applicable."""
    try:
        u = urlsplit(offer['url'])
        if u.scheme != 'https' or u.netloc != HOSTS.get(offer['merchant_id']) or u.fragment:
            return False
        if offer['merchant_id'] == 'paco':
            return not u.query and bool(re.fullmatch(r'/it/[^/]+/\d+-[^/]+\.htm', u.path))
        if offer['merchant_id'] == 'isola-dei-tesori':
            return not u.query and bool(re.fullmatch(r'/prodotto/[^/]+/\d+\.html', u.path))
        return bool(re.fullmatch(r'/products/[^/]+', u.path)) and bool(re.fullmatch(r'variant=\d+', u.query))
    except (KeyError, TypeError, ValueError):
        return False


def stamp(value):
    try:
        d = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
        return d if d.tzinfo is not None else None
    except (AttributeError, ValueError):
        return None


def record(old, offer, code, now):
    previous = stamp(old.get('checked_at'))
    same = old.get('url') == offer['url']
    dead = code in (404, 410)
    confirmations = 0
    if dead:
        confirmations = 1
        if same and old.get('status') in (404, 410) and previous and 6*3600 <= (now-previous).total_seconds() <= 7*86400:
            confirmations = min(2, old.get('confirmations', 0)+1)
        elif same and old.get('status') in (404, 410) and previous and 0 <= (now-previous).total_seconds() < 6*3600:
            confirmations = old.get('confirmations', 1)
    return dict(url=offer['url'], checked_at=now.isoformat(), status=code, confirmations=confirmations)


def blocked(entry, offer, now):
    checked = stamp(entry.get('checked_at'))
    return bool(checked and 0 <= (now-checked).total_seconds() <= 7*86400
                and entry.get('url') == offer['url'] and entry.get('status') in (404, 410)
                and entry.get('confirmations', 0) >= 2)


def candidates(offers, cache, now, limit=24):
    buckets = defaultdict(list)
    for o in offers:
        if not safe_product(o):
            continue
        entry = cache.get(o['id'], {})
        checked = stamp(entry.get('checked_at'))
        age = (now-checked).total_seconds() if checked else float('inf')
        interval = 7*86400 if entry.get('status') == 200 else (86400 if entry.get('confirmations', 0) >= 2 else 6*3600)
        if entry.get('url') != o['url'] or age >= interval:
            pending = entry.get('url') == o['url'] and entry.get('status') in (404, 410) and entry.get('confirmations') == 1
            buckets[o['merchant_id']].append((0 if pending else 1, checked.isoformat() if checked else '', o['id'], o))
    for rows in buckets.values():
        rows.sort(key=lambda x: x[:3])
    selected = []
    while len(selected) < limit and any(buckets.values()):
        for merchant in sorted(buckets):
            if buckets[merchant] and len(selected) < limit:
                selected.append(buckets[merchant].pop(0)[3])
    return selected


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never follow a Location, even if it appears to be a merchant.


class Checker:
    def __init__(self):
        self.opener = urllib.request.build_opener(NoRedirect())
        self.robots = {}
        self.stopped = set()

    def allowed(self, url):
        u = urlsplit(url); origin = u.scheme+'://'+u.netloc
        if origin not in self.robots:
            parser = urllib.robotparser.RobotFileParser()
            try:
                req = urllib.request.Request(origin+'/robots.txt', headers={'User-Agent': UA})
                with self.opener.open(req, timeout=5) as response:
                    raw = response.read(512001)
                    if len(raw) > 512000: raise ValueError('Robots too large')
                    parser.parse(raw.decode('utf-8', errors='replace').splitlines())
                self.robots[origin] = parser
            except Exception:
                self.robots[origin] = None  # No permission inferred from failure.
        parser = self.robots[origin]
        # Respect explicit throttles by skipping this bounded run rather than ignoring them.
        return bool(parser and not parser.crawl_delay(UA) and not parser.request_rate(UA) and parser.can_fetch(UA, url))

    def head(self, offer):
        if not safe_product(offer): return 'unsafe_url'
        host = urlsplit(offer['url']).netloc
        if host in self.stopped: return 'host_paused'
        if not self.allowed(offer['url']): return 'robots_unverified_or_disallowed'
        req = urllib.request.Request(offer['url'], method='HEAD', headers={'User-Agent': UA})
        try:
            with self.opener.open(req, timeout=5) as response:
                return response.status
        except urllib.error.HTTPError as error:
            code = error.code
            error.close()
            if code in (403, 429): self.stopped.add(host)
            return code
        except Exception:
            return 'network_error'


def apply(catalog, cache, now, fetch, limit=24, budget=60, pause=.5):
    ids = {o['id'] for o in catalog['offers']}
    cache = {k:v for k,v in cache.items() if k in ids}
    started = time.monotonic(); results = Counter(); attempted = 0
    for offer in candidates(catalog['offers'], cache, now, limit):
        if time.monotonic()-started >= budget: break
        code = fetch(offer)
        cache[offer['id']] = record(cache.get(offer['id'], {}), offer, code, now)
        attempted += 1; results[str(code)] += 1
        if pause: time.sleep(pause)
    suppressed = [o for o in catalog['offers'] if blocked(cache.get(o['id'], {}), o, now)]
    suppressed_ids = {o['id'] for o in suppressed}
    output = dict(catalog, offers=[o for o in catalog['offers'] if o['id'] not in suppressed_ids])
    report = dict(checked_at=now.isoformat(), input_offers=len(catalog['offers']), published_offers=len(output['offers']),
        attempted_this_run=attempted, results_this_run=dict(results), cached_product_urls=len(cache),
        suppressed=[dict(id=o['id'],merchant=o['merchant'],checked_at=cache[o['id']]['checked_at'],status=cache[o['id']]['status']) for o in suppressed],
        method='Campione progressivo, massimo 24 HEAD dirette per ciclo e budget 60 secondi; robots rispettato, niente redirect, cookie o link affiliati. Sospensione solo dopo due HTTP 404/410 a distanza di almeno sei ore, per lo stesso URL, entro sette giorni. HTTP200 non certifica prezzo, stock o identità; errori di rete, blocchi e redirect restano inconcludenti.')
    return output, cache, report


def build():
    path = ROOT/'site/data/catalog.json.gz'; state = ROOT/'automation/link-health-cache.json'
    catalog = json.loads(gzip.decompress(path.read_bytes()))
    cache = json.loads(state.read_text()) if state.exists() else {}
    output, cache, report = apply(catalog, cache, dt.datetime.now(dt.timezone.utc), Checker().head)
    path.write_bytes(gzip.compress(json.dumps(output, ensure_ascii=False, separators=(',', ':')).encode(), mtime=0))
    state.write_text(json.dumps(cache, ensure_ascii=False, indent=2)+'\n')
    (ROOT/'site/data/link-health.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    build()
