"""Curated brand landing pages backed by exact catalog brand labels."""
import gzip
import json
from pathlib import Path
from html import escape as h
from urllib.parse import urlencode
try:
    from .build_product_pages import page, fresh
    from .build_matched_pages import groups, slug_for, product_label, merchant_url
except ImportError:
    from build_product_pages import page, fresh
    from build_matched_pages import groups, slug_for, product_label, merchant_url

try:
    from automation.list_schema import append_list_schema
except ImportError:
    from list_schema import append_list_schema


try:
    from automation.report_link import error_link
except ImportError:
    from report_link import error_link

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://offerte4zampe.it/'
BRANDS = [('monge','Monge'),('royal-canin','Royal Canin'),('farmina','Farmina'),('natural-trainer','Natural Trainer'),('purina-pro-plan','Purina Pro Plan')]


def select(offers, brand, limit=24):
    rows = [o for o in offers if o.get('brand','').strip().casefold()==brand.casefold() and fresh(o) and o.get('available') and o.get('price',0)>0 and str(o.get('url','')).startswith('https://')]
    # Alphabetical source rotation is an editorial sample, never a price ranking.
    byshop = {shop:sorted([o for o in rows if o['merchant']==shop],key=lambda o:(product_label(o).casefold(),o['id'])) for shop in sorted({o['merchant'] for o in rows})}
    picked = []
    while len(picked)<limit and any(byshop.values()):
        for shop in byshop:
            if byshop[shop] and len(picked)<limit:
                picked.append(byshop[shop].pop(0))
    return rows,picked


def build():
    offers = json.loads(gzip.decompress((ROOT/'site/data/catalog.json.gz').read_bytes()))['offers']
    template = (ROOT/'site/chi-siamo.html').read_text()
    matched = groups(offers)
    links, list_items = [], []
    for suffix,brand in BRANDS:
        slug = 'marca-'+suffix
        rows,picked = select(offers,brand)
        if len(rows)<12:
            if (ROOT/f'site/{slug}.html').exists():
                body = '<section class="pagehero"><div class="wrap"><h1>'+h(brand)+': catalogo da aggiornare</h1><p>Non ci sono dati recenti sufficienti per questa selezione.</p><a href="confronta-cibo.html">Cerca nel catalogo →</a></div></section>'
                (ROOT/f'site/{slug}.html').write_text(page(template,slug,brand+': dati da aggiornare','Dati recenti non sufficienti.',body).replace('content="index,follow"','content="noindex,follow"'))
            continue
        cards,items = [],[]
        for i,o in enumerate(picked):
            key=(o.get('gtin'),format(o['weight_kg'],'.12g'),o['brand'].strip().lower()) if o.get('weight_kg') else None
            comparison = slug_for(key) if key in matched else None
            more = f'<a href="{comparison}.html">Stesso codice e formato in più negozi →</a>' if comparison else ''
            unit = f'{o["price"]/o["weight_kg"]:.2f} €/kg' if o.get('weight_kg') else 'Peso netto non verificato: prezzo/kg non calcolato'
            rel = 'sponsored noopener noreferrer' if o.get('affiliate_url') else 'noopener noreferrer'
            disclosure = '<p class="micro">Possiamo ricevere una commissione, senza costi aggiuntivi per te.</p>' if o.get('affiliate_url') else ''
            label = product_label(o)
            cards.append(f'<article class="catalog-card"><p class="micro">{h(o["merchant"])} · {h(o["brand"])}</p><h2><a class="product-title-link" href="{h(merchant_url(o),quote=True)}" rel="{rel}">{h(label)}</a></h2><p>{h(o.get("variant") or "Formato non specificato")}</p><p class="catalog-price"><strong>{o["price"]:.2f} €</strong></p><p>{unit} · spedizione esclusa</p><p class="micro">Disponibile al rilevamento · recupero dati: <time datetime="{h(o["checked_at"],quote=True)}">{h(o["checked_at"])}</time></p>{more}<a class="btn secondary" href="{h(merchant_url(o),quote=True)}" target="_blank" rel="{rel}">Vai al negozio ↗</a>{disclosure}{error_link(o)}</article>')
            items.append({'@type':'ListItem','position':i+1,'name':label,'url':BASE+comparison if comparison else merchant_url(o)})
        shop_count=len({o['merchant_id'] for o in rows})
        title=brand+': prodotti, formati e prezzi rilevati'
        query=h(urlencode({'brand':brand}),quote=True)
        body=f'<section class="pagehero"><div class="wrap"><nav aria-label="Percorso"><a href="index.html">Home</a> / <a href="marche.html">Marche</a></nav><h1>{h(title)}</h1><p>{len(rows)} offerte disponibili al rilevamento in {shop_count} negozi del catalogo, {sum(bool(o.get("weight_kg")) for o in rows)} con peso netto dichiarato.</p></div></section><section class="section"><div class="wrap"><p class="notice">Questa pagina usa la marca esatta «{h(brand)}» indicata nei cataloghi. Le altre linee commerciali possono avere un’etichetta diversa e non sono incluse automaticamente. Non è l’intero assortimento del produttore né una classifica di qualità. Prezzi rilevati, non in tempo reale; spedizione esclusa.</p><h2>Come leggere la selezione {h(brand)}</h2><p>Controlla nome completo, ricetta, fascia di età e formato. Prodotti della stessa marca non sono equivalenti: non confrontare automaticamente alimenti diversi usando soltanto il prezzo al kg. Per diete veterinarie e necessità nutrizionali segui le indicazioni del veterinario.</p><p>Mostriamo fino a 24 offerte, alternate per negozio e in ordine alfabetico all’interno di ogni fonte. Le commissioni non determinano la selezione. Quando codice GTIN, marca e peso netto coincidono, trovi un collegamento al confronto dello stesso formato.</p><a class="btn" href="confronta-cibo.html?{query}">Cerca tutte le offerte {h(brand)} →</a><div class="catalog-grid">'+''.join(cards)+'</div><h2>Strumenti utili prima di acquistare</h2><p><a href="confronta-cibo.html#manual-tool">Confronta costo/kg e costo giornaliero</a> con la razione del produttore; <a href="calcolatore.html">organizza il budget</a> oppure leggi <a href="costo-crocchette-cane.html">come calcolare il costo mensile delle crocchette</a>.</p><p><a href="chi-siamo.html">Metodo e fonti</a> · <a href="marche.html">Altre marche del catalogo</a></p></div></section>'
        data={'@context':'https://schema.org','@graph':[{'@type':'ItemList','name':title,'itemListElement':items},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':BASE+url} for i,(name,url) in enumerate([('Home',''),('Marche','marche'),(brand,slug)])]}]}
        output=page(template,slug,title,'Prezzi rilevati e formati '+brand+' nelle fonti del catalogo. Verifica ricetta, confezione e spedizione prima di acquistare.',body)
        output=output.replace('</head>','<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script></head>')
        (ROOT/f'site/{slug}.html').write_text(output)
        list_items.append((brand,BASE+slug))
        links.append(f'<li><a href="{slug}.html">{h(brand)}</a> · {len(rows)} offerte rilevate · {shop_count} negozi</li>')
    body='<section class="pagehero"><div class="wrap"><h1>Marche: trova i tuoi prodotti abituali</h1><p>Una prima selezione di marche con dati sufficienti nei cataloghi. Ogni pagina distingue nomi, formati, fonti e data di recupero.</p></div></section><section class="section"><div class="wrap content"><ul>'+''.join(links)+'</ul><p>Non sono tutte le marche disponibili. <a href="confronta-cibo.html">Usa il filtro marca nel comparatore</a> per esplorare il catalogo completo.</p></div></section>'
    (ROOT/'site/marche.html').write_text(append_list_schema(page(template,'marche','Marche di prodotti per animali: prezzi e formati','Marche con dati di catalogo sufficienti: ricette, confezioni, negozi e prezzi rilevati.',body),'Marche nel catalogo',list_items))
    home=ROOT/'site/index.html'
    before=home.read_text()
    if 'href="marche.html"' not in before:
        before=before.replace('<div class="brand-links" id="home-brands">','<p><a href="marche.html">Esplora le pagine delle marche →</a></p><div class="brand-links" id="home-brands">')
        home.write_text(before)
    print('Brand pages generated:',len(links))


if __name__ == '__main__':
    build()
