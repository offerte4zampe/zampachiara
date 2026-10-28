"""Consolidate older generated GTIN pages into the canonical product routes."""
import gzip,json,re
from pathlib import Path
try:
    from .build_matched_pages import groups,slug_for
except ImportError:
    from build_matched_pages import groups,slug_for
ROOT=Path(__file__).resolve().parents[1]

def build():
    catalog=json.loads(gzip.decompress((ROOT/'site/data/catalog.json.gz').read_bytes()))
    redirects=[]
    for key,rows in groups(catalog['offers']).items():
        slug=rows[0].get('product_slug')
        if not slug:continue
        old=slug_for(key);target='/prodotto/'+slug
        redirects.extend([f'/{old} {target} 301',f'/{old}.html {target} 301'])
        path=ROOT/'site'/(old+'.html')
        if path.exists():
            text=path.read_text();text=re.sub(r'(<link rel="canonical" href=")[^"]+',r'\g<1>https://offerte4zampe.it'+target,text)
            text=text.replace('content="index,follow"','content="noindex,follow"');path.write_text(text)
    path=ROOT/'site/_redirects';old=path.read_text() if path.exists() else ''
    old=re.sub(r'# canonical-products:start.*?# canonical-products:end\n?','',old,flags=re.S)
    path.write_text(old.rstrip()+'\n# canonical-products:start\n'+'\n'.join(sorted(redirects))+'\n# canonical-products:end\n')
    print('Legacy product redirects:',len(redirects))
if __name__=='__main__':build()
