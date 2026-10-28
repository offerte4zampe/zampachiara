"""Public record of evidenced technical corrections, never invented user reports."""
import json
from html import escape as h
from pathlib import Path
try:
    from .build_product_pages import page
except ImportError:
    from build_product_pages import page

ROOT = Path(__file__).resolve().parents[1]


def render(template, entries, report, link_health=None, store_audit=None):
    cards = []
    for entry in entries:
        cards.append(f'<article class="panel"><p class="micro"><time datetime="{h(entry["date"],quote=True)}">{h(entry["date"])}</time> · {h(entry["origin"])}</p><h2>{h(entry["title"])}</h2><p>{h(entry["detail"])}</p><a href="{h(entry["evidence"],quote=True)}" rel="noopener noreferrer" target="_blank">Modifica documentata ↗</a></article>')
    stamp = h(report.get('checked_at') or 'Non disponibile')
    summary = '<p>Controlli automatici non ancora disponibili.</p>'
    if report.get('checked_at'):
        summary = f'<p>Controllo del {stamp}: {report["input_offers"]} offerte esaminate, {report["published_offers"]} ammesse alla pubblicazione, {len(report["quarantined"])} sospese. {len(report["repaired"])} campi di peso non validi rimossi, senza modificare i prezzi.</p>'
    body = '<section class="pagehero"><div class="wrap"><nav aria-label="Percorso"><a href="index.html">Home</a> / <a href="chi-siamo.html">Metodo</a></nav><h1>Correzioni e qualità dei dati</h1><p>Un registro delle modifiche documentate e dei controlli eseguiti prima di pubblicare il catalogo.</p></div></section><section class="section"><div class="wrap content">'+''.join(cards)+'<h2>Controlli automatici del catalogo</h2>'+summary+'<p>Escludiamo prezzi non validi, identificativi duplicati, collegamenti non validi e rilevazioni oltre 36 ore o con date incoerenti. Un peso non valido viene rimosso: non ricaviamo un peso netto da quello di trasporto.</p><p>Il controllo dei prezzi anomali usa soltanto lo stesso GTIN valido, marca e peso netto. Una differenza oltre il 50% viene sospesa soltanto quando almeno due altri negozi indipendenti hanno prezzi concordanti entro il 20%. Confronti per nomi simili o mediane generiche di categoria non bastano. Una sospensione è un dato da verificare, non la prova di un errore o di una promozione falsa.</p><p>Questi controlli non certificano ricette, disponibilità o prezzo al pagamento. I link dei negozi non vengono visitati automaticamente da questo controllo: eventuali errori HTTP richiedono una verifica separata. Non dichiariamo risolte segnalazioni di utenti senza averle ricevute e verificate.</p><h2>Hai trovato un errore?</h2><p>Usa il collegamento accanto all’offerta oppure <a href="segnala-errore.html">prepara una segnalazione</a>. Il modulo apre una bozza nel tuo programma email; non invia automaticamente messaggi. Non promettiamo un tempo di risposta che non possiamo garantire.</p><p><a href="confronta-cibo.html">Torna al comparatore</a> · <a href="chi-siamo.html">Metodo e fonti</a> · <a href="contatti.html">Contatti</a></p></div></section>'
    if link_health and link_health.get('checked_at'):
        health = '<h2>Verifica progressiva dei link</h2><p>Ultimo ciclo: '+h(link_health['checked_at'])+'. '+str(link_health['attempted_this_run'])+' esiti nel campione, '+str(link_health['cached_product_urls'])+' URL nel registro, '+str(len(link_health['suppressed']))+' offerte sospese per collegamenti non trovati confermati.</p><p>Controlliamo soltanto gli URL diretti dei prodotti, senza seguire redirect o link affiliati. Il campione è limitato: non certifica tutti i collegamenti del catalogo. Due risposte HTTP 404/410 distanziate di almeno sei ore sono necessarie per una sospensione; timeout, redirect, blocchi e metodi non supportati restano inconcludenti. Una risposta HTTP200 non dimostra prezzo o disponibilità corretti.</p><p><a href="data/link-health.json">Esiti e limiti del controllo</a>.</p>'
        body = body.replace('<h2>Hai trovato un errore?</h2>', health+'<h2>Hai trovato un errore?</h2>')
    if store_audit:
        names={'bauzaar':'Bauzaar','webpet':'WebPet','animaliapet':'Animaliapet','isola-dei-tesori':'Isola dei Tesori','paco':'Paco Pet Shop'}
        rows=''.join('<tr><th scope="row">'+h(names.get(s['id'],s['id']))+'</th><td>'+h(s.get('source_status','unknown'))+'</td><td>'+str(s['offers'])+'</td><td>'+str(s['sample_verified'])+'</td><td>'+str(s['sample_inconclusive'])+'</td><td>'+str(s['sample_discrepancies'])+'</td></tr>' for s in store_audit['stores'])
        section='<h2>Verifica indipendente dei cinque negozi</h2><p>Ultimo controllo: '+h(store_audit['checked_at'])+'. I campi di tutte le offerte sono controllati; un campione a rotazione viene confrontato con varianti o schede originali. Il controllo non dipende dalle segnalazioni degli utenti.</p><div class="catalog-table"><table><thead><tr><th>Negozio</th><th>Importazione</th><th>Offerte</th><th>Pagine verificate</th><th>Inconcludenti</th><th>Discrepanze aperte</th></tr></thead><tbody>'+rows+'</tbody></table></div><p>Il campione non certifica tutte le pagine del negozio. URL validi e importazioni riuscite non provano prezzi, formato o stock. Le varianti non identificabili restano non verificate; non vengono abbinate per somiglianza del nome.</p><p><a href="data/store-audit.json">Riscontri, fonti e limiti del controllo per negozio</a>.</p>'
        body=body.replace('<h2>Hai trovato un errore?</h2>',section+'<h2>Hai trovato un errore?</h2>')
    return page(template, 'correzioni', 'Correzioni e controlli sui dati', 'Registro delle correzioni documentate e metodo dei controlli automatici sui prezzi e formati del catalogo.', body)


def build():
    template = (ROOT/'site/chi-siamo.html').read_text()
    entries = json.loads((ROOT/'automation/corrections.json').read_text())['entries']
    path = ROOT/'site/data/catalog-quarantine.json'
    report = json.loads(path.read_text()) if path.exists() else {}
    health_path = ROOT/'site/data/link-health.json'
    health = json.loads(health_path.read_text()) if health_path.exists() else None
    audit_path=ROOT/'site/data/store-audit.json'
    store_audit=json.loads(audit_path.read_text()) if audit_path.exists() else None
    (ROOT/'site/correzioni.html').write_text(render(template, entries, report, health, store_audit))


if __name__ == '__main__':
    build()
