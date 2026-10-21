"""Curated line pages: explicit brand labels and line token, no recipe matching."""
import datetime
import gzip
import json
import math
import pathlib
import re
from html import escape as h
from urllib.parse import urlencode
try:
    from .build_product_pages import page, fresh
except ImportError:
    from build_product_pages import page, fresh
ROOT=pathlib.Path(__file__).resolve().parents[1]
SLUG='linea-monge-bwild'
SOURCE='https://www.monge.it/i-nostri-marchi/'

def select(offers,now=None):
    rows=[o for o in offers if o.get('brand','').strip().casefold() in ('monge','monge bwild')
          and re.search(r'\bbwild\b',o.get('title',''),re.I) and fresh(o,now)
          and o.get('available') is True and isinstance(o.get('price'),(int,float))
          and math.isfinite(o['price']) and o['price']>0 and isinstance(o.get('id'),str)
          and str(o.get('url','')).startswith('https://')]
    byshop={s:sorted([o for o in rows if o['merchant']==s],key=lambda o:(o['title'].casefold(),o['id'])) for s in sorted({o['merchant'] for o in rows})}
    picked=[]
    while len(picked)<24 and any(byshop.values()):
        for s in byshop:
            if byshop[s] and len(picked)<24:picked.append(byshop[s].pop(0))
    return rows,picked

def render(template,catalog,now=None):
    rows,picked=select(catalog.get('offers',[]),now)
    shops=len({o['merchant'] for o in rows})
    if len(rows)<12 or shops<2:
        body='<section class="pagehero"><div class="wrap"><h1>Monge BWild: dati da aggiornare</h1><p>La selezione richiede almeno dodici offerte recenti in due negozi. Non mostriamo prezzi precedenti come attuali.</p><a href="marca-monge.html">Esplora Monge</a></div></section>'
        return page(template,SLUG,'Monge BWild: dati da aggiornare','Dati recenti insufficienti per questa selezione.',body).replace('content="index,follow"','content="noindex,follow"')
    cards=[]
    for o in picked:
        target='prodotto.html?'+urlencode({'id':o['id']})
        weight=o.get('weight_kg')
        unit=f'{o["price"]/weight:.2f} €/kg' if isinstance(weight,(int,float)) and math.isfinite(weight) and weight>0 else 'Peso netto non verificato: costo/kg non calcolato'
        cards.append(f'<article class="catalog-card"><p class="micro">{h(o["merchant"])} · {h(o["brand"])}</p><h2><a class="product-title-link" href="{h(target,quote=True)}">{h(o["title"])}</a></h2><p>{h(o.get("variant") or "Formato non specificato")}</p><p class="catalog-price"><strong>{o["price"]:.2f} €</strong></p><p>{unit} · spedizione esclusa</p><p class="micro">Disponibile al rilevamento: <time datetime="{h(o["checked_at"],quote=True)}">{h(o["checked_at"])}</time></p><a class="btn secondary" href="{h(target,quote=True)}">Confronta questo prodotto</a></article>')
    title='Monge BWild: ricette e formati, prezzi nei negozi'
    body=f'<section class="pagehero"><div class="wrap"><nav aria-label="Percorso"><a href="index.html">Home</a> / <a href="marche.html">Marche</a> / <a href="marca-monge.html">Monge</a></nav><h1>{title}</h1><p>{len(rows)} offerte recenti disponibili al rilevamento in {shops} negozi del catalogo. Prezzi non in tempo reale; spedizione esclusa.</p></div></section><section class="section"><div class="wrap"><div class="content"><h2>Una linea, prodotti diversi</h2><p>Il produttore presenta BWild come una linea Monge per cani e gatti, con alimenti secchi e umidi e proposte Low Grain e Grain Free. Queste indicazioni descrivono una famiglia commerciale: non rendono equivalenti ricette, confezioni o impieghi. La scelta nutrizionale va valutata con il veterinario.</p><p>Fonte ufficiale della denominazione e della gamma: <a href="{SOURCE}" target="_blank" rel="noopener noreferrer">i marchi Monge</a>, consultata il 21 ottobre 2026. Non riproduciamo promesse sanitarie o percentuali di ingredienti come caratteristiche comuni di ogni prodotto.</p><h2>Quali offerte entrano in questa pagina</h2><p>Includiamo soltanto etichette marca Monge o Monge BWild con la parola BWild esplicita nel titolo del catalogo. I nomi abbreviati e le altre linee rimangono fuori: questa selezione non copre necessariamente tutto il catalogo ufficiale. Non abbiamo identificato una corrispondenza solo perché due nomi sono simili.</p><p>Mostriamo al massimo 24 offerte, alternate per negozio e alfabetiche nella singola fonte. Una riga è un’offerta, non necessariamente un prodotto distinto. Le commissioni non influenzano selezione e ordine. L’assenza di un negozio non dimostra che non venda la linea.</p><h2>Prima di confrontare il prezzo</h2><p>Leggi il titolo completo: specie, età indicata, ricetta e formato. Low Grain e Grain Free restano denominazioni distinte. Verifica inoltre se il prezzo riguarda una confezione o un multipack: non moltiplichiamo quantità ricostruite dal nome e non convertiamo un formato incerto in un peso presunto.</p><p>Il prezzo al kg appare solo con peso netto verificato. Serve a leggere il costo della confezione, non a misurare qualità o durata: alimenti diversi possono richiedere quantità diverse. Non pubblichiamo un minimo complessivo della linea come se tutte le ricette fossero intercambiabili.</p><p>Apri la singola scheda per controllare quali negozi riportano quello specifico prodotto e formato. Da lì puoi scegliere il negozio, verificare la stima di spedizione, consultare lo storico osservato o aggiungere una confezione alla lista. Disponibilità, condizioni e totale vanno sempre confermati nel negozio prima dell’acquisto.</p></div><div class="catalog-grid">'+''.join(cards)+'</div><div class="content"><h2>Strumenti per una scelta verificabile</h2><p><a href="stesso-prodotto-formato-gtin.html">Controlla identità e formato</a>, <a href="prezzo-confezione-o-prezzo-kg.html">leggi il costo della confezione e al kg</a> e <a href="spedizione-gratuita-conviene.html">valuta la spedizione</a>. Nessun codice promozionale o risparmio garantito è implicito nei prezzi riportati.</p><p><a href="marca-monge.html">Altri prodotti Monge</a> · <a href="chi-siamo.html">Metodo, fonti e affiliazioni</a>.</p></div></div></section>'
    output=page(template,SLUG,title,'Offerte della linea Monge BWild: ricette e formati distinti, prezzi datati e accesso al confronto del singolo prodotto.',body)
    schema={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':'https://offerte4zampe.it/'+slug} for i,(name,slug) in enumerate([('Home',''),('Marche','marche'),('Monge','marca-monge'),('BWild',SLUG)])]}
    return output.replace('</head>','<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script></head>')

def build():
    catalog=json.loads(gzip.decompress((ROOT/'site/data/catalog.json.gz').read_bytes()))
    (ROOT/f'site/{SLUG}.html').write_text(render((ROOT/'site/chi-siamo.html').read_text(),catalog))
if __name__=='__main__':build()
