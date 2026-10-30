"""Canonical internal product links with a compatibility fallback for unmapped rows."""
import re
from urllib.parse import urlencode

def product_url(o):
    slug=o.get('product_slug','')
    if re.fullmatch(r'[a-z0-9-]{1,200}',slug):return '/prodotto/'+slug
    return '/prodotto.html?'+urlencode({'id':o['id']})
