"""Generate small title-only metadata shards; never export prices or merchant links."""
import hashlib
import json
import pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]

def build(catalog):
    rows, ambiguous = {}, set()
    for offer in catalog.get('offers', []):
        key, title = offer.get('id'), offer.get('title')
        if not isinstance(key, str) or not 0 < len(key) <= 200 or not isinstance(title, str) or not title.strip() or len(title) > 240:
            continue
        title = title.strip()
        if key in rows and rows[key] != title:
            ambiguous.add(key)
        rows[key] = title
    shards = {f'{i:02x}': {} for i in range(256)}
    for key, title in sorted(rows.items()):
        if key not in ambiguous:
            shards[hashlib.sha256(key.encode()).hexdigest()[:2]][key] = title
    return shards

def write(catalog, directory):
    directory.mkdir(parents=True, exist_ok=True)
    for shard, titles in build(catalog).items():
        (directory/(shard+'.json')).write_text(json.dumps(titles, ensure_ascii=False, separators=(',', ':'))+'\n')

if __name__ == '__main__':
    import gzip
    write(json.loads(gzip.decompress((ROOT/'site/data/catalog.json.gz').read_bytes())), ROOT/'site/data/product-meta')
