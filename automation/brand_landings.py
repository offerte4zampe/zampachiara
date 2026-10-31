"""Stable landing slugs for exact catalog brand labels, without guessing aliases."""
import collections
import hashlib
import re
import unicodedata
from functools import lru_cache

LEGACY={'Monge':'monge','Royal Canin':'royal-canin','Farmina':'farmina','Natural Trainer':'natural-trainer','Purina Pro Plan':'purina-pro-plan'}

def legacy_brand_pages(offers, minimum=5):
    counts=collections.Counter(str(o.get('brand') or '').strip() for o in offers)
    names=sorted((name for name,count in counts.items() if name and count>=minimum),key=str.casefold)
    taken={slug:name for name,slug in LEGACY.items()};result=[]
    for name in names:
        slug=LEGACY.get(name) or re.sub(r'[^a-z0-9]+','-',unicodedata.normalize('NFKD',name).encode('ascii','ignore').decode().lower()).strip('-') or 'marca'
        if slug in taken and taken[slug]!=name:
            slug+='-'+hashlib.sha256(name.encode()).hexdigest()[:8]
        taken[slug]=name;result.append((slug,name))
    return result

try:
    from .build_product_catalog import canonical_brand as product_brand
except ImportError:
    from build_product_catalog import canonical_brand as product_brand

@lru_cache(maxsize=4096)
def canonical_brand(value):
    return product_brand(value)

FISHING_BRANDS = {'shimano','rapala','gamakatsu','mustad','stonfo'}

def in_scope(offer):
    return str(offer.get('brand') or '').strip().casefold() not in FISHING_BRANDS

def brand_pages(offers, minimum=5):
    return legacy_brand_pages([{**o, 'brand': canonical_brand(o.get('brand'))} for o in offers if in_scope(o)], minimum)
