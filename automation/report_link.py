"""Build a local report link without affiliate tracking URLs or user identifiers."""
from html import escape
from urllib.parse import urlencode


def error_link(offer):
    fields = {key:str(offer.get(source) or '')[:limit] for key,source,limit in [('id','id',100),('title','title',240),('shop','merchant',100),('price','price',30),('checked','checked_at',60)]}
    return '<p class="micro"><a href="segnala-errore.html?'+escape(urlencode(fields),quote=True)+'">Prezzo o dati sbagliati? Segnala</a></p>'
