# Verifica Search Console — 26 ottobre 2026

Proprietà https://offerte4zampe.it/, account del progetto. Lettura UI autenticata del report Pagine, aggiornato al 23 ottobre 2026; tutti gli esempi delle cinque categorie letti, non soltanto la prima pagina. Nessuna richiesta AdSense, convalida correzione o richiesta di indicizzazione inviata.

## Dati Google
56 URL indicizzati e 595 esclusi:
- 180 noindex:89/segnala-errore.html,89/segnala-errore,1/carrello-risparmio,1/carrello-risparmio.html. Tutte esclusioni intenzionali confermate nei metadati.
- 73 alternate canonical: tutti /confronta-cibo con parametri di ricerca/filtro; canonical del documento verso/confronta-cibo, comportamento voluto.
- 70 reindirizzamenti: versioni.html delle pagine e ricerche del comparatore; hosting Workers Assets html_handling auto-trailing-slash. Nessuna categoria errore redirect nel report. Non occorre indicizzare gli alias.
- 265 rilevati non indicizzati:258/prezzi-* e7 guide/pagine (confrontare-prezzi-lettiere,correzioni,leggere-storico-prezzi,osservatorio-prezzi,prezzo-confezione-o-prezzo-kg,spedizione-gratuita-conviene,stesso-prodotto-formato-gtin).
- 7 scansionati non indicizzati:marca-purina-pro-plan,prezzi-08009470085250-ff80aeb073,marca-royal-canin e.html,marca-natural-trainer e.html,1 segnala-errore con parametri. Quattro pagine canoniche editoriali/comparative, due alias .html e un modulo volutamente noindex.

## Confronto con repository corrente
site-quality.json osservato26 ottobre06:54UTC:466 HTML,326 indicizzabili e326 canonical univoci, zero problemi delle regole statiche (non certifica ogni aspetto SEO).
Le cinque partizioni sitemap contengono esattamente326 URL univoci, tutti coincidenti con l’inventario indicizzabile: nessun noindex, query o alias.html in sitemap.
Fra 265 URL rilevati,185 sono ancora indicizzabili oggi;80 sono ora confronti ritirati/noindex perché mancano dati recenti sufficienti. build_matched_pages.py mantiene questi vecchi URL senza mostrare prezzi scaduti; esempio/prezzi-03700260009832-f96df87d68. Il conteggio Google precedente non va interpretato come265errori da correggere.
Sitemap nel pannello: riuscita, inviata18 ottobre, ultima lettura24 ottobre,334 URL rilevati allora.326 attuali e334 letti in precedenza sono snapshot differenti.

## Ispezioni puntuali e test live
/marca-royal-canin: scansioneGooglebot smartphone 21 ottobre00:49:24, consentita, recupero positivo, indicizzazione consentita e canonical dichiarato corretto; Google ha scelto URL controllato. Rimane scansionata non indicizzata. Test live 26 ottobre14:41: URL disponibile per Google, pagina può essere indicizzata, breadcrumb valido.
/confrontare-prezzi-lettiere: rilevata da sitemap, nessuna scansione nell’indice. Test live 26 ottobre14:43: URL disponibile per Google, pagina può essere indicizzata, breadcrumb valido.
Questi test non garantiscono che Google scelga di indicizzare le pagine e non sostituiscono test live di ogni URL. Non è emerso un blocco tecnico da correggere nelle categorie dell’email o nei due test. La copertura limitata resta un problema concreto di visibilità: prioritizzare pagine stabili, utili e ben collegate; non rimuovere le esclusioni volute né dichiarare risolte le scelte d’indicizzazione di Google.

Fonti interpretative: https://support.google.com/webmasters/answer/7440203 e https://support.google.com/webmasters/answer/9012289 . Nessuna modifica al codice o al deploy necessaria per questa verifica.
