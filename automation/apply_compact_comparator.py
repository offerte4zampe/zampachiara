"""Keep comparison tools focused; move manual A/B inputs to Budget."""
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def region(html,element_id,tag='div'):
    start=re.search(r'<'+tag+r'\b[^>]*\bid="'+re.escape(element_id)+r'"[^>]*>',html)
    if not start:return None
    depth=1
    for token in re.finditer(r'</?'+tag+r'\b[^>]*>',html[start.end():]):
        depth+=-1 if token[0].startswith('</') else 1
        if depth==0:return start.start(),start.end()+token.end()
    raise ValueError('Unbalanced '+element_id)

def comparator(html):
    if 'id="catalog-extra-filters"' not in html:
        manual=html.find('id="manual-tool"')
        if manual>=0:
            start=html.rfind('<section class="section" style="padding-top:15px">',0,manual)
            end=html.index('<section class="section alt">',manual)
            html=html[:start]+html[end:]
        start,end=region(html,'catalog-filters');filters=html[start:end];opening=filters.index('>')+1;query_end=filters.index('</div>',opening)+6
        query=filters[opening:query_end];extra=filters[query_end:-6]
        load=re.search(r'<button\b[^>]*id="catalog-load"[^>]*>.*?</button>',html,re.S)[0]
        load=re.sub(r'>[^<]*</button>','>Cerca nel catalogo</button>',load)
        first=html.index('<div class="notice">',html.index('<main'));preamble=html[first:html.index('<button id="catalog-load"',first)]
        status=re.search(r'<p\b[^>]*id="catalog-status"[^>]*>.*?</p>',preamble,re.S)[0]
        preamble=preamble.replace(status,'')
        status=re.sub(r'>[^<]*</p>','>Prezzi rilevati: verifica sempre il totale nel negozio.</p>',status)
        replacement='<div id="catalog-filters" class="panel catalog-filters">'+query+load+'<details id="catalog-extra-filters"><summary>Filtri avanzati</summary><div class="catalog-filter-body">'+extra+'</div></details></div>'+status+'<p class="micro"><a href="/carrello-risparmio">Lista risparmio · <span data-basket-count>0</span> confezioni</a></p>'
        html=html[:first]+replacement+html[end:]
        html=html.replace('</main>','<section class="section"><div class="wrap"><p><a href="/calcolatore#manual-tool">Calcola costo giornaliero e confronto A/B →</a></p><details class="catalog-method"><summary>Fonti, metodo e lista risparmio</summary>'+preamble+'</details></div></section></main>')
        shipping=re.search(r'<div class="panel shipping-controls">',html)
        if shipping:
            marked=html[:shipping.start()]+html[shipping.start():].replace('<div class="panel shipping-controls">','<div id="catalog-shipping" class="panel shipping-controls">',1)
            a,b=region(marked,'catalog-shipping');inside=marked[a:b];inside=inside[inside.index('>')+1:-6]
            html=marked[:a]+'<details class="panel shipping-controls" id="catalog-shipping"><summary>Stima spedizione</summary>'+inside+'</details>'+marked[b:]
        html=html.replace('Cerca tra le offerte importate dai negozi, filtra per marca e confronta fino a quattro confezioni. Per gli alimenti puoi anche stimare il costo giornaliero con la razione del produttore.','Cerca un prodotto e confronta prezzi, formati e negozi.')
        # Keep educational detail after the results, in the linked guide and calculator.
        html=re.sub(r'<section class="section alt"><div class="wrap content"><span class="kicker">Prima di acquistare</span>.*?</section>','<section class="section alt"><div class="wrap content"><h2>Prima di acquistare</h2><p>Controlla ricetta, confezione e totale nel negozio. <a href="/prezzo-confezione-o-prezzo-kg">Guida al prezzo per kg</a> · <a href="/calcolatore#manual-tool">Costo giornaliero A/B</a>.</p></div></section>',html,flags=re.S)
    if 'id="catalog-bottom-tools"' not in html:
        share_id=html.find('id="catalog-share"')
        start=html.rfind('<div class="buttons">',0,share_id)
        fallback=region(html,'catalog-share-fallback')
        share=html[start:fallback[1]];html=html[:start]+html[fallback[1]:]
        a,b=region(html,'catalog-shipping','details');shipping=html[a:b];html=html[:a]+html[b:]
        tools='<section class="section"><div class="wrap" id="catalog-bottom-tools"><h2>Affina e condividi il confronto</h2>'+shipping+share+'</div></section>'
        html=html.replace('</main>',tools+'</main>')
    # Remove the duplicate saved-list summary in the collapsible method text.
    html=re.sub(r'<p[^>]*>\s*(?:La tua lista risparmio|<a[^>]*>La tua lista risparmio).*?</p>', '', html, flags=re.S)
    html=html.replace('Prezzi rilevati: verifica sempre il totale nel negozio.','Verifica il totale nel negozio prima di acquistare.')
    html=html.replace('Primi 24 prodotti: precedenza ai confronti con più negozi, poi nome. Prezzi rilevati, spedizione esclusa.','Primi 24 prodotti: precedenza ai confronti con più negozi, poi nome.')
    html=html.replace('Prezzi rilevati dai cataloghi dei negozi.','Dati dai cataloghi dei negozi.')
    return html

def budget(html,manual):
    if 'id="manual-tool"' not in html:html=html.replace('</main>',manual+'</main>')
    script='<script src="assets/food.js" defer></script>'
    if script not in html:html=html.replace('</body>',script+'</body>')
    return html

def main():
    manual=(ROOT/'automation/partials/manual-food.html').read_text()
    catalog=ROOT/'site/confronta-cibo.html';catalog.write_text(comparator(catalog.read_text()).replace('<script src="assets/food.js" defer></script>',''))
    page=ROOT/'site/calcolatore.html';page.write_text(budget(page.read_text(),manual))
    for page in (ROOT/'site').rglob('*.html'):
        before=page.read_text();after=re.sub(r'(?P<prefix>href=["\'])(?:/)?confronta-cibo(?:\.html)?#manual-tool',r'\g<prefix>/calcolatore#manual-tool',before)
        if after!=before:page.write_text(after)
if __name__=='__main__':main()
