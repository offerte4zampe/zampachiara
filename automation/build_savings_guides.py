"""Editorial guides with reproducible current catalog examples, never invented prices."""
import datetime as dt
import gzip
import json
import math
import re
from html import escape as h
from pathlib import Path
try:
    from .build_product_pages import page, fresh
    from .build_matched_pages import groups, merchant_url, product_label, slug_for
except ImportError:
    from build_product_pages import page, fresh
    from build_matched_pages import groups, merchant_url, product_label, slug_for

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://offerte4zampe.it/'
REVIEW = '2026-10-20'


def eligible(o, now):
    return (fresh(o, now) and o.get('available') is True and isinstance(o.get('price'), (int,float))
            and math.isfinite(o['price']) and o['price'] > 0 and isinstance(o.get('weight_kg'), (int,float))
            and math.isfinite(o['weight_kg']) and o['weight_kg'] > 0 and str(o.get('url','')).startswith('https://'))


def food_examples(offers, now):
    rows = sorted((o for o in offers if eligible(o, now)
        and re.search(r'crocchett|alimento secco|cibo secco',o.get('category',''),re.I)
        and re.search(r'cane|cani|\bdog\b',o['title']+' '+o.get('category',''),re.I)
        and not re.search(r'veterinar|renal|diabet|medicat|integrator|farmac|diet',o['title']+' '+o.get('category',''),re.I)),
        key=lambda o:(o['title'].casefold(),o['id']))
    picked=[]; merchants=set()
    for o in rows:
        if o['merchant_id'] not in merchants:
            picked.append(o);merchants.add(o['merchant_id'])
        if len(picked)==3:break
    return picked


def litter_examples(offers, now):
    candidates=groups([o for o in offers if eligible(o,now)])
    choices=[(key,rows) for key,rows in candidates.items() if all('lettier' in (o['title']+' '+o.get('category','')).casefold() for o in rows)]
    return sorted(choices,key=lambda item:(product_label(item[1][0]).casefold(),item[0]))[:2]


def money(value): return f'{value:.2f}'.replace('.',',')+' €'


def source_link(o):
    return f'<a class="product-title-link" href="{h(merchant_url(o),quote=True)}" rel="{"sponsored noopener noreferrer" if o.get("affiliate_url") else "noopener noreferrer"}">{h(product_label(o))}</a>'


def document(template, slug, title, description, content, now):
    body=f'<section class="pagehero"><div class="wrap"><nav aria-label="Percorso"><a href="index.html">Home</a> / <a href="guide-risparmio.html">Guide al risparmio</a></nav><h1>{h(title)}</h1><p>{h(description)}</p><p class="micro">A cura della redazione Offerte a 4 Zampe · metodo rivisto il {REVIEW} · esempi aggiornati il <time datetime="{h(now.isoformat(),quote=True)}">{h(now.isoformat()[:16].replace("T"," "))} UTC</time>.</p></div></section><section class="section"><div class="wrap content">{content}<h2>Fonti, limiti e aggiornamento</h2><p>Gli esempi vengono dai feed ufficiali e cataloghi pubblici importati, con prezzo, peso netto e data per ogni riga. La selezione è alfabetica e alterna i negozi, senza dipendere dalle commissioni. Non rappresenta tutto il mercato. I calcoli non sono test nutrizionali o consigli veterinari.</p><p>I prezzi sono rilevazioni datate e la spedizione è esclusa dalle tabelle. Controlla sempre ricetta, confezione, disponibilità e totale nel negozio. I link Bauzaar e Isola dei Tesori possono generare una commissione senza costi aggiuntivi per te. <a href="chi-siamo.html">Metodo e fonti dei cataloghi</a> · <a href="correzioni.html">Controlli e correzioni</a>.</p><p><a href="guide-risparmio.html">Altre guide pratiche</a> · <a href="confronta-cibo.html">Cerca il tuo prodotto</a> · <a href="carrello-risparmio.html">Confronta la lista della spesa</a>.</p></div></section>'
    out=page(template,slug,title,description,body)
    schema={'@context':'https://schema.org','@graph':[{'@type':'Article','headline':title,'description':description,'dateModified':now.isoformat(),'author':{'@type':'Organization','name':'Redazione Offerte a 4 Zampe','url':BASE+'chi-siamo'},'mainEntityOfPage':BASE+slug},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':i+1,'name':name,'item':BASE+url} for i,(name,url) in enumerate([('Home',''),('Guide al risparmio','guide-risparmio'),(title,slug)])]}]}
    return out.replace('</head>','<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('</',r'<\/')+'</script></head>')


def food_content(offers,now):
    rows=[]
    for o in food_examples(offers,now):
        unit=o['price']/o['weight_kg'];day=unit*.25
        rows.append(f'<tr><td>{source_link(o)}<br>{h(o["merchant"])}</td><td>{o["weight_kg"]:g} kg</td><td>{money(o["price"])}</td><td>{money(unit)}/kg</td><td>{money(day)}</td><td>{money(day*30)}</td><td>{h(o["checked_at"][:16].replace("T"," "))} UTC</td></tr>')
    table='<p>Nessun esempio recente con peso netto verificabile: usa il comparatore per controllare il catalogo.</p>'
    if rows: table='<div class="guide-table" tabindex="0" role="region" aria-label="Esempi di costo con razione ipotetica"><table><caption>Razione ipotetica uguale di 250 g/giorno, spedizione esclusa</caption><thead><tr><th>Prodotto e fonte</th><th>Peso netto</th><th>Confezione</th><th>Costo/kg</th><th>Al giorno</th><th>Per 30 giorni</th><th>Rilevazione</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>'
    return '<h2>Il prezzo del sacco non basta</h2><p>Il costo mensile dipende da tre dati: prezzo della confezione, peso netto e grammi effettivamente consumati al giorno. Un sacco economico può contenere meno prodotto; un prezzo al kg inferiore può richiedere un esborso iniziale maggiore. Separare questi aspetti aiuta a confrontare la spesa senza trasformare un prezzo in un giudizio sulla qualità dell’alimento.</p><h2>La formula da usare sulla tua confezione</h2><p>Prezzo/kg = prezzo della confezione ÷ kg netti. Costo giornaliero = prezzo/kg × grammi al giorno ÷ 1.000. Per una stima su 30 giorni moltiplica il risultato non arrotondato per 30. La spesa di spedizione va aggiunta una volta all’ordine, non a ogni porzione.</p><p>Usa il peso netto dichiarato: il peso di spedizione comprende altri elementi e non misura quanto cibo acquisti. Se il formato non è verificabile, il sito evita il prezzo/kg. Non ricavare una razione dal prezzo: leggi l’etichetta e segui le indicazioni del veterinario per il tuo animale.</p><h2>Esempi con prezzi realmente rilevati</h2><p>La tabella usa una quantità ipotetica di 250 g al giorno soltanto per rendere riproducibile il calcolo. Non è una razione consigliata né una previsione per un cane di una certa taglia. Le ricette elencate sono diverse: la stessa quantità non dimostra equivalenza energetica o nutrizionale.</p>'+table+'<h2>Dal consumo al denaro da spendere</h2><p>Il costo di 30 giorni descrive il prodotto consumato nell’ipotesi scelta. Il pagamento al negozio riguarda invece confezioni intere: puoi dover comprare un sacco oggi e usarne una parte il mese prossimo. Per il budget considera entrambi i numeri e controlla spazio disponibile, conservazione e tempi indicati dal produttore. Comprare più confezioni solo per raggiungere una soglia di spedizione può aumentare la spesa subito necessaria.</p><h2>Quando due alimenti si possono confrontare</h2><p>Per cercare lo stesso prodotto tra negozi usa codice GTIN, marca e formato, poi verifica la ricetta sull’etichetta. Il solo nome commerciale può nascondere differenze. Per confrontare alimenti diversi, il costo giornaliero ha senso soltanto con le rispettive razioni adatte al tuo animale: non usare una porzione uguale come prova di convenienza nutrizionale.</p><h2>Fai il calcolo con i tuoi dati</h2><p>Nel comparatore apri il calcolo giornaliero dell’offerta e inserisci la razione che hai verificato. Il campo parte vuoto: non assegniamo una dieta automaticamente. Per quantità e spedizione usa la <a href="carrello-risparmio.html">lista risparmio</a>, che confronta ordini completi solo quando assortimento e condizioni sono stimabili.</p><a class="btn" href="confronta-cibo.html#manual-tool">Apri il calcolatore →</a>'


def litter_content(offers,now):
    tables=[]
    for key,rows in litter_examples(offers,now):
        lines=[]
        for o in sorted(rows,key=lambda o:(o['merchant'].casefold(),o['id'])):
            lines.append(f'<tr><td>{h(o["merchant"])}</td><td>{source_link(o)}</td><td>{o["weight_kg"]:g} kg</td><td>{money(o["price"])}</td><td>{money(o["price"]/o["weight_kg"])}/kg</td><td>{h(o["checked_at"][:16].replace("T"," "))} UTC</td></tr>')
        tables.append(f'<h3>Codice GTIN {h(key[0])} · {h(rows[0]["brand"])}</h3><div class="guide-table" tabindex="0" role="region" aria-label="Prezzi dello stesso formato di lettiera"><table><caption>Stesso GTIN, marca e peso netto dichiarati; spedizione esclusa</caption><thead><tr><th>Negozio</th><th>Prodotto</th><th>Formato</th><th>Confezione</th><th>Costo/kg</th><th>Rilevazione</th></tr></thead><tbody>{"".join(lines)}</tbody></table></div><p><a href="{slug_for(key)}.html">Apri tutte le offerte dello stesso formato</a>.</p>')
    examples=''.join(tables) or '<p>Non sono disponibili confronti recenti con identità e peso sufficienti. Non accostiamo automaticamente lettiere con nomi simili.</p>'
    return '<h2>Parti dalla confezione esatta</h2><p>Per confrontare una lettiera controlla materiale, variante, profumazione e formato. Due confezioni dello stesso marchio possono essere prodotti diversi. Nel catalogo raggruppiamo soltanto GTIN, marca e peso netto coincidenti; questo controllo non sostituisce la lettura dell’etichetta, ma evita di unire offerte solo per somiglianza del nome.</p><h2>Litri e chilogrammi misurano cose diverse</h2><p>Il litro esprime un volume, il chilogrammo una massa. Non convertiamo automaticamente 10 litri in 10 kg: materiali diversi possono avere pesi diversi a parità di volume. Quando il catalogo dichiara entrambi, manteniamo il peso netto esplicito. Se ci sono solo litri, il prezzo/kg resta non disponibile. Anche il peso di spedizione non è un sostituto del contenuto netto.</p><h2>Due confronti tratti dal catalogo</h2><p>Questi esempi sono selezionati in ordine alfabetico tra i gruppi recenti di lettiere, senza privilegiare commissioni o differenze di prezzo. L’ordine dei negozi è alfabetico. Non sono una classifica di qualità o una promessa sul negozio più economico dopo la spedizione.</p>'+examples+'<h2>Il totale cambia con la lista della spesa</h2><p>Una confezione dal prezzo più basso può appartenere a un ordine con spedizione maggiore. Se compri più prodotti nello stesso negozio, la soglia di gratuità e l’eventuale peso massimo si applicano all’ordine. Sommare una spedizione a ogni prodotto sovrastima il totale; ignorarla sottostima quanto pagherai. Località particolari, servizi aggiuntivi e condizioni non verificate possono impedire una stima affidabile.</p><p>La <a href="carrello-risparmio.html">lista risparmio</a> applica la spedizione una volta al subtotale e confronta soltanto gli assortimenti completi con identità verificabile. Se un negozio ha una parte dei prodotti richiesti, non mostriamo quel subtotale come alternativa all’intera spesa. Le tariffe hanno una data di verifica e il checkout resta il riferimento finale.</p><h2>Prova prima una quantità realistica</h2><p>Valuta quante confezioni ti servono e quanto spazio hai prima di aggiungere articoli per superare una soglia. Il prezzo/kg è utile per confrontare formati verificati, ma non dimostra quanto durerà una lettiera: durata e consumo dipendono anche dall’uso e dalle indicazioni del produttore. Non traduciamo quindi il prezzo in un costo mensile universale.</p><h2>Una verifica rapida prima del pagamento</h2><p>Apri la scheda del negozio e ricontrolla nome completo, variante, quantità selezionata, prezzo della confezione e spese per la tua destinazione. I multipack con base del prezzo non chiara vengono esclusi finché la quantità non è verificata. Se trovi una discrepanza, usa la segnalazione accanto al prezzo: la bozza mostra i dati dell’offerta prima di aprire il tuo programma email.</p><a class="btn" href="confronta-cibo.html?q=lettiera">Cerca una lettiera nel comparatore →</a>'


GUIDES = [('costo-crocchette-cane','Quanto costano le crocchette al mese?','Prezzo/kg e costo giornaliero con esempi reali e una razione modificabile: separa consumo, confezioni e spedizione.',food_content),('confrontare-prezzi-lettiere','Come confrontare i prezzi delle lettiere','Formati in kg e litri, stesso prodotto e spesa complessiva: esempi rilevati dal catalogo e controlli prima del checkout.',litter_content)]


def build():
    now=dt.datetime.now(dt.timezone.utc)
    catalog=json.loads(gzip.decompress((ROOT/'site/data/catalog.json.gz').read_bytes()))
    template=(ROOT/'site/chi-siamo.html').read_text()
    for slug,title,description,render in GUIDES:
        (ROOT/f'site/{slug}.html').write_text(document(template,slug,title,description,render(catalog['offers'],now),now))
    links=''.join(f'<article class="panel"><h2><a href="{slug}.html">{h(title)}</a></h2><p>{h(description)}</p></article>' for slug,title,description,_ in GUIDES)
    body='<section class="pagehero"><div class="wrap"><h1>Guide pratiche al risparmio per cani e gatti</h1><p>Metodi riproducibili ed esempi del catalogo, con fonti, date e limiti. Nessuna classifica nutrizionale.</p></div></section><section class="section"><div class="wrap content">'+links+'<p><a href="confronta-cibo.html">Confronta prezzi</a> · <a href="chi-siamo.html">Metodo editoriale</a>.</p></div></section>'
    (ROOT/'site/guide-risparmio.html').write_text(page(template,'guide-risparmio','Guide pratiche al risparmio per animali','Guide con esempi reali per confrontare confezioni, costo al kg e spese di spedizione.',body))


if __name__=='__main__':build()
