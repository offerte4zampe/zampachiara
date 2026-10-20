"""Publish a curated, stable set of product pages; never fuzzy-match recipes."""
import gzip, json, re, datetime
from pathlib import Path
from html import escape as h, unescape
from urllib.parse import quote

try:
    from automation.list_schema import append_list_schema
except ImportError:
    from list_schema import append_list_schema


try:
    from automation.report_link import error_link
except ImportError:
    from report_link import error_link

ROOT=Path(__file__).resolve().parents[1]
PRODUCTS=[
 ('monge-maxi-adult-pollo','bauzaar:56820456423749'),
 ('monge-medium-adult-pollo','bauzaar:56820456063301'),
 ('monge-adult-manzo-riso','bauzaar:56820470546757'),
 ('monge-adult-cat-pollo','bauzaar:58411855446341'),
 ('royal-canin-medium-adult','bauzaar:56820427817285'),
 ('royal-canin-maxi-adult','bauzaar:58411852628293'),
 ('pro-plan-large-athletic-agnello','bauzaar:58411845517637'),
 ('pro-plan-medium-sensitive-skin-salmone','bauzaar:58411854332229')]

def same_product(a,b):
    # Only a merchant's exact product name and brand; variants remain explicit.
    return (a['merchant'],a['title'],a['brand'])==(b['merchant'],b['title'],b['brand'])

def fresh(offer, now=None):
    now=now or datetime.datetime.now(datetime.timezone.utc)
    try:
        stamp=datetime.datetime.fromisoformat(offer['checked_at'].replace('Z','+00:00'))
        return stamp.tzinfo is not None and -300 <= (now-stamp).total_seconds() <= 36*3600
    except (ValueError,KeyError,TypeError):return False


def page(template,slug,title,description,body):
    out=re.sub(r'<main\b.*?</main>',lambda _:f'<main id="main" data-product-page>{body}</main>',template,flags=re.S)
    out=re.sub(r'<title>.*?</title>',lambda _:f'<title>{h(title)} | Offerte a 4 Zampe</title>',out)
    for key in ['name="description"','property="og:description"']:
        out=re.sub('(<meta '+key+' content=")[^"]*',lambda m:m[1]+h(description,quote=True),out)
    out=re.sub(r'(<meta property="og:title" content=")[^"]*',lambda m:m[1]+h(title,quote=True),out)
    out=out.replace('https://offerte4zampe.it/chi-siamo','https://offerte4zampe.it/'+slug).replace(' aria-current="page"','')
    return out

def build():
    catalog=json.loads(gzip.decompress((ROOT/'site/data/catalog.json.gz').read_bytes()))
    offers=catalog['offers']; byid={o['id']:o for o in offers}; template=(ROOT/'site/chi-siamo.html').read_text(); cards=[]; urls=[]; list_items=[]
    for slug,oid in PRODUCTS:
        seed=byid.get(oid)
        if not seed:
            previous=ROOT/f'site/{slug}.html'
            old=re.search(r'<h1[^>]*>(.*?)</h1>',previous.read_text(),re.S) if previous.exists() else None
            label=unescape(re.sub('<[^>]+>','',old[1])).split(' — ')[0] if old else slug.replace('-',' ').title()
            body=f'<section class="pagehero"><div class="wrap"><h1>{h(label)}</h1><p>Questa offerta non è presente nell’ultimo catalogo. Prezzo e disponibilità non sono confermati: non mostriamo quelli delle rilevazioni precedenti come attuali.</p><a class="btn" href="confronta-cibo.html">Cerca nel catalogo aggiornato →</a></div></section>'
            previous.write_text(page(template,slug,label,'Prezzo e disponibilità da verificare nel catalogo aggiornato.',body).replace('content="index,follow"','content="noindex,follow"'))
            continue
        rows=sorted((o for o in offers if same_product(seed,o)),key=lambda o:((o.get('weight_kg') or 9999),o['price']))
        title=seed['title']+' — prezzo e formati'; desc='Prezzi rilevati, formati e costo al kg di '+seed['title']+'. Controlla disponibilità e spedizione prima di acquistare.'
        table=[]
        for o in rows:
            weight=o.get('weight_kg'); unit=f'{o["price"]/weight:.2f} €/kg'.replace('.',',') if weight else 'Peso non verificato'
            recent=fresh(o)
            availability=('Disponibile' if o['available'] else 'Non disponibile') if recent else 'Dato da aggiornare'
            price=f'{o["price"]:.2f} €' if recent else 'Non aggiornato'
            unit=unit if recent else 'Non aggiornato'
            buy=(f'<a class="btn secondary" data-metric="merchant_click" data-merchant="{h(o["merchant"])}" href="{h(o.get("affiliate_url") or o["url"],quote=True)}" target="_blank" rel="sponsored noopener noreferrer">Vedi nel negozio ↗</a>' if recent and o['available'] else 'Acquisto da verificare')
            table.append(f'<tr><td>{h(o.get("variant") or "Formato non specificato")}</td><td>{price}</td><td>{unit}</td><td>{availability}</td><td>{h(o["checked_at"][:10])}</td><td>{buy}{error_link(o)}</td></tr>')
        body=f'''<section class="pagehero"><div class="wrap"><span class="eyebrow">{h(seed['brand'])} · Prezzi dal catalogo</span><h1>{h(title)}</h1><p>{h(desc)}</p><a class="btn secondary" href="prodotti.html">← Tutti i prodotti in evidenza</a></div></section><section class="section"><div class="wrap content"><h2>Formati rilevati presso {h(seed['merchant'])}</h2><p>Questa scheda raccoglie le varianti con lo stesso nome e marca nel catalogo di {h(seed['merchant'])}. Non è un confronto verificato fra negozi: senza un codice EAN non uniamo automaticamente prodotti dai nomi simili.</p><div style="overflow-x:auto"><table><thead><tr><th>Formato</th><th>Prezzzo prodotto</th><th>Prezzo al kg</th><th>Disponibilità rilevata</th><th>Rilevato il</th><th>Negozio</th></tr></thead><tbody>{''.join(table)}</tbody></table></div><p class="notice">Spedizione esclusa. Prezzo e disponibilità possono cambiare: il totale valido è quello mostrato dal negozio al pagamento. I link Bauzaar e Isola dei Tesori sono commerciali: possiamo ricevere una commissione, senza costi aggiuntivi per te.</p><h2>Come confrontare questo prodotto</h2><p>Per {h(seed['title'])}, controlla che il nome completo, la ricetta e la fascia di età riportati sulla confezione coincidano. Una confezione più grande può avere un prezzo al kg inferiore, ma richiede più spazio e deve essere consumata nei tempi indicati dal produttore.</p><p>Il prezzo al kg divide il prezzo rilevato per il peso esplicito della variante; non converte litri in kg e non comprende la spedizione. Non indica da solo il costo giornaliero: quello dipende dalla razione adatta al tuo animale.</p><h2>Vuoi cercarlo anche negli altri cataloghi?</h2><p>Il comparatore cerca il testo nei cataloghi importati. I risultati possono includere ricette e formati diversi: verifica le confezioni prima di confrontare i prezzi.</p><a class="btn" href="confronta-cibo.html?q={quote(seed['title'])}">Cerca nel comparatore →</a><p class="micro">Aggiornamento previsto ogni sei ore. Ogni riga mostra la data effettiva del prezzo. <a href="chi-siamo.html">Metodo di raccolta</a>.</p></div></section>'''.replace('Prezzzo','Prezzo')
        (ROOT/f'site/{slug}.html').write_text(page(template,slug,title,desc,body)); urls.append(slug)
        list_items.append((seed['title'],'https://offerte4zampe.it/'+slug))
        cards.append(f'<article class="panel"><p class="micro">{h(seed["brand"])}</p><h2 style="font-size:1.2rem"><a href="{slug}.html">{h(seed["title"])}</a></h2><p>{len(rows)} formati rilevati · {h(seed["merchant"])}</p><a href="{slug}.html">Prezzi e formati →</a></article>')
    body='<section class="pagehero"><div class="wrap"><span class="eyebrow">Prodotti in evidenza</span><h1>Prezzi e formati, prodotto per prodotto</h1><p>Una selezione editoriale di alimenti presenti nei cataloghi importati. Non è una classifica di qualità o popolarità e non sono consigli nutrizionali.</p></div></section><section class="section"><div class="wrap"><p>Ogni scheda distingue confezioni, disponibilità e prezzo al kg. Le offerte fra negozi restano separate quando non possiamo verificarne l’equivalenza.</p><p><a href="confronti-prodotti.html">Stesso GTIN e formato: confronta più negozi →</a></p><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:20px">'+''.join(cards)+'</div></div></section>'
    (ROOT/'site/prodotti.html').write_text(append_list_schema(page(template,'prodotti','Prodotti per animali: prezzi e formati','Schede dei prodotti con prezzi reali, formati e data di rilevamento.',body),'Prodotti in evidenza',list_items)); urls.append('prodotti')
    sitemap=ROOT/'site/sitemap.xml'; xml=sitemap.read_text()
    for slug,_ in PRODUCTS:
        xml=re.sub(r'<url><loc>https://offerte4zampe.it/'+re.escape(slug)+r'</loc>.*?</url>','',xml,flags=re.S)
    for slug in urls:
        xml=re.sub(r'<url><loc>https://offerte4zampe.it/'+re.escape(slug)+r'</loc>.*?</url>','',xml,flags=re.S)
        xml=xml.replace('</urlset>',f'<url><loc>https://offerte4zampe.it/{slug}</loc><lastmod>{catalog["generated_at"][:10]}</lastmod></url>\n</urlset>')
    sitemap.write_text(xml)
    print('Generated',len(cards),'product pages and index')
if __name__=='__main__': build()
