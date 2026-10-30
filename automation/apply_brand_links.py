"""Link only published brand landings; retain search filters on other parameters."""
import json
import re
from html import escape,unescape
from pathlib import Path
from urllib.parse import parse_qs,urlsplit
try:
    from .build_home_data import replace_region
except ImportError:
    from build_home_data import replace_region
ROOT=Path(__file__).resolve().parents[1]

def apply(html,pages):
    def link(match):
        value=urlsplit(unescape(match[2]));query=parse_qs(value.query)
        if value.scheme or value.netloc or value.path.lstrip('/') not in ('confronta-cibo','confronta-cibo.html') or set(query)!={'brand'}:return match[0]
        target=pages.get(query['brand'][0])
        return 'href='+match[1]+escape(target or '/marche',quote=True)+match[1]
    html=re.sub(r'href=([\"\'])(.*?)\1',link,html)
    if 'id="home-brands"' in html:
        html=re.sub(r' data-brand-pages="[^"]*"','',html)
        html=html.replace('id="home-brands"','id="home-brands" data-brand-pages="'+escape(json.dumps(pages,ensure_ascii=False),quote=True)+'"')
        content='<h2>Marche del catalogo</h2><details><summary>Tutte le marche con almeno cinque offerte recenti ('+str(len(pages))+')</summary><div class="brand-links">'+''.join('<a href="'+url+'">'+escape(name)+'</a>' for name,url in sorted(pages.items(),key=lambda x:x[0].casefold()))+'</div></details>'
        if 'id="home-all-brands"' in html:html=replace_region(html,'home-all-brands',content)
        else:html=html.replace('</main>','<section class="section"><div class="wrap" id="home-all-brands">'+content+'</div></section></main>')
    return html

def main():
    pages=json.loads((ROOT/'site/data/brand-pages.json').read_text())
    for path in (ROOT/'site').rglob('*.html'):
        before=path.read_text();after=apply(before,pages)
        if after!=before:path.write_text(after)
if __name__=='__main__':main()
