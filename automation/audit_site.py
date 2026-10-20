"""Deterministic static quality gates for generated public HTML."""
import datetime as dt
import gzip
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
BASE='offerte4zampe.it'


class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.lang='';self.canonical=[];self.robots='';self.title=[];self.description=[];self.viewport=False
        self.h1=0;self.main=0;self.skip=False;self.links=[];self.images=[];self.schemas=[];self._title=False;self._script=False;self._script_type='';self._buffer=''
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang','')
        if tag=='link' and 'canonical' in a.get('rel','').split():self.canonical.append(a.get('href',''))
        if tag=='meta' and a.get('name')=='robots':self.robots=a.get('content','').lower()
        if tag=='meta' and a.get('name')=='description':self.description.append(a.get('content','').strip())
        if tag=='meta' and a.get('name')=='viewport':self.viewport=bool(a.get('content'))
        if tag=='title':self._title=True;self._buffer=''
        if tag=='h1':self.h1+=1
        if tag=='main':self.main+=1
        if tag=='a':
            self.links.append(a)
            if 'skip' in a.get('class','').split() and a.get('href','').startswith('#'):self.skip=True
        if tag=='img':self.images.append(a)
        if tag=='script':
            self._script=True;self._script_type=a.get('type','');self._buffer=''
    def handle_data(self,data):
        if self._title or self._script:self._buffer+=data
    def handle_endtag(self,tag):
        if tag=='title':
            self.title.append(self._buffer.strip());self._title=False;self._buffer=''
        if tag=='script':
            if self._script_type=='application/ld+json':self.schemas.append(self._buffer)
            self._script=False;self._script_type='';self._buffer=''


def inspect(site):
    files=sorted(site.glob('*.html'));issues=[];pages=[];canonicals={}
    for path in files:
        # Search Console ownership tokens are machine verification files, not pages.
        if path.name.startswith('google') and path.name.endswith('.html'):
            continue
        p=Page(path.read_text())
        rel=path.name
        local=[]
        if p.lang!='it':local.append('html_lang_it')
        if not p.viewport:local.append('viewport')
        if len(p.title)!=1 or not p.title[0]:local.append('one_nonempty_title')
        if len(p.description)!=1 or not p.description[0]:local.append('one_nonempty_description')
        if p.main!=1:local.append('one_main')
        if p.h1!=1:local.append('one_h1')
        if not p.skip:local.append('skip_link')
        indexable='noindex' not in p.robots and 'none' not in p.robots
        if indexable:
            if len(p.canonical)!=1:local.append('one_canonical')
            elif p.canonical:
                u=urlsplit(p.canonical[0])
                if u.scheme!='https' or u.netloc!=BASE or u.query or u.fragment:local.append('clean_internal_canonical')
                elif p.canonical[0] in canonicals:local.append('unique_canonical')
                else:canonicals[p.canonical[0]]=rel
        for link in p.links:
            href=link.get('href','')
            rels=set(link.get('rel','').split())
            if link.get('target')=='_blank' and not {'noopener','noreferrer'}<=rels:local.append('safe_new_tab')
            if ('tc.tradetracker.' in href or 'amazon.' in href and ('tag=' in href or '/dp/' in href)) and 'sponsored' not in rels:local.append('commercial_rel_sponsored')
        for image in p.images:
            if 'alt' not in image:local.append('image_alt')
            if not image.get('width') or not image.get('height'):local.append('image_dimensions')
        for raw in p.schemas:
            try:json.loads(raw)
            except (ValueError,TypeError):local.append('valid_json_ld')
        local=sorted(set(local))
        issues.extend({'page':rel,'rule':rule} for rule in local)
        pages.append({'page':rel,'indexable':indexable,'canonical':p.canonical[0] if len(p.canonical)==1 else None,'issues':local})
    return {'pages_scanned':len(pages),'indexable_pages':sum(p['indexable'] for p in pages),'unique_canonicals':len(canonicals),'issues':issues,'rule_counts':dict(sorted(Counter(i['rule'] for i in issues).items())),'pages':pages}


def build():
    result=inspect(ROOT/'site')
    try:
        catalog=json.loads(gzip.decompress((ROOT/'site/data/catalog.json.gz').read_bytes()))
        observed_at=catalog.get('generated_at')
    except (OSError,ValueError,EOFError):
        observed_at=None
    report={'method_version':1,'observed_at':observed_at,**result}
    (ROOT/'site/data/site-quality.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Static quality:',report['pages_scanned'],'pages;',len(report['issues']),'issues')
    if report['issues']:
        for item in report['issues'][:30]:print(item['page'],item['rule'])
        raise SystemExit(1)


if __name__=='__main__':build()
