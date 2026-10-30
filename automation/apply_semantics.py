"""Preserve page hierarchy and product card semantics in generated HTML."""
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HEADING=re.compile(r'<h([1-6])\b([^>]*)>(.*?)</h\1>',re.S|re.I)
def apply(html):
    # Product names are subordinate to section headings.
    def card(m):
        if not re.search(r'class="[^"]*(?:catalog-card|home-deal|spotlight-product)',m[0]):return m[0]
        return re.sub(r'<(/?)h2\b',r'<\1h3',m[0])
    html=re.sub(r'<article\b[^>]*>.*?</article>',card,html,flags=re.S)
    previous=0
    def heading(m):
        nonlocal previous
        if not re.sub(r'<[^>]*>','',m[3]).strip():return ''
        level=int(m[1])
        if previous and level>previous+1:level=previous+1
        previous=level
        return '<h'+str(level)+m[2]+'>'+m[3]+'</h'+str(level)+'>'
    def main_region(m):
        nonlocal previous
        previous=0
        return HEADING.sub(heading,m[0])
    if '<main' in html:return re.sub(r'<main\b[^>]*>.*?</main>',main_region,html,flags=re.S)
    return HEADING.sub(heading,html)
if __name__=='__main__':
    changed=0
    for p in (ROOT/'site').rglob('*.html'):
        before=p.read_text();after=apply(before)
        if before!=after:p.write_text(after);changed+=1
    print('Semantic hierarchy updated:',changed)
