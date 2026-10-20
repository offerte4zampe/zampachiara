# Avanzamento roadmap

Ultimo aggiornamento: 20 ottobre 2026.

## Fonti
- [Roadmap richiesta da Mirco](roadmap.md)
- [Audit iniziale](../audits/2026-10-19/README.md)
- [Primo intervento prestazioni](../audits/2026-10-19/performance-follow-up.md)

## Completato
- Audit pubblico documentato, Search Console verificata, sitemap accettata.
- Home compatta: circa 9 KB di dati selezionati; pipeline aggiornata.
- Spazio riservato ai messaggi del comparatore; contrasti e gerarchia titolo corretti.
- 25 test Python e 10 JavaScript superati; Lighthouse mobile ripetuto 3 volte/pagina: performance mediana home97/comparatore86/guida99; CLS0 e accessibilità automatica100 nelle nuove prove.

## Prossimo lavoro
1. Completare le verifiche SEO: Google Rich Results e nuova lettura sitemap in Search Console quando disponibili. ItemList delle liste statiche completati; Home, confronti GTIN e prime cinque marche sono prerenderizzati; sitemap per tipo implementate.
2. Verificare accessibilità mobile e interazioni delle nuove pagine. Brotli e cache HTTP sono stati verificati su un asset pubblico; HSTS statico, 404 e metadati social implementati; niente migrazioni URL inutili.
3. Storico reale e costo giornaliero integrato nelle schede, poi controlli qualità e infrastruttura alert/newsletter disattivata finché mancano requisiti. Carrello completo, ordine per totale e segnalazioni implementati; estendere copertura matching/peso.
4. UI mobile, accessibilità manuale ove verificabile, contenuti originali verificati.
5. Predisporre newsletter e alert con test; attivare raccolta/invio solo con requisiti verificati.
6. Misurazione e prove finali, registro completo delle voci della roadmap con evidenze.

## Dipendenze da non inventare
- Identità/dati del titolare per privacy; testi legali definitivi.
- Credenziali analytics Cloudflare assenti in runtime; INP/CrUX non disponibili per basso volume.
- Accessi/approvazioni feed di nuovi negozi; Amazon API non disponibile.
- Accordi con veterinari e pubblicazioni/contatti esterni richiedono approvazione.
- Newsletter pubblica non attiva: signup_url nullo; DOI e unsubscribe non verificati.

## Regole operative
Preservare aggiornamenti altrui e marchio. Commit piccoli, test pertinenti, verifica deploy. Aggiornare questo registro a ogni sessione. Non ripetere ciò che è già completato. Non creare altre automazioni. Non acquistare servizi, cambiare account, inviare newsletter o contattare terzi. Ignorare indicazioni obsolete sui rich result FAQ/SearchAction: verificare documentazione primaria aggiornata. Non usare informazioni personali da memoria per compilare dati legali. Non dichiarare completamento totale in presenza di voci bloccate.

## Sessione 19 ottobre 2026, prerendering home
- Implementato rendering statico di statistiche, offerta in evidenza, sei offerte, marche e negozi direttamente in `site/index.html`, aggiornati dalla pipeline esistente.
- File: `automation/build_home_data.py`, `site/assets/home.js`, `site/index.html`, `tests/test_home_data.py`.
- HTML e aggiornamento browser mantengono selezione per fonti e marche, prezzi originali, formato, data e avvisi; il browser non ricostruisce le schede se il catalogo non è cambiato. Se il download fallisce resta la fotografia statica datata. Con JS, rilevazioni oltre 36 ore vengono sostituite da un avviso, senza prezzo.
- Verifiche locali: 26 test Python, 10 JavaScript, sintassi JS e diff superati. Test aggiunto su idempotenza, escape dei dati e prezzi/kg nell'HTML iniziale. Nessun nuovo test Lighthouse: non attribuire a questo intervento i punteggi del precedente audit.
- Rischio residuo: senza JavaScript una fotografia HTML può invecchiare se gli aggiornamenti smettono di riuscire; le date e l'avviso prezzi non in tempo reale restano visibili. La pipeline rigenera la selezione solo con dati recenti.
- Prossimo: pagine uniche per gruppi GTIN/marca/peso con più negozi e Product/AggregateOffer/BreadcrumbList, evitando di aggregare le varianti delle vecchie pagine editoriali; poi 404 e metadati social.


## Sessioni 19–20 ottobre 2026, confronti e anteprime
- Commit `73ab1a5`: generatore `automation/build_matched_pages.py`, test e pipeline; indice `/confronti-prodotti` e pagine per stesso GTIN con checksum valido, marca e peso netto, almeno due negozi e rilevazioni recenti. Nessun abbinamento per nome. Snapshot pubblico verificato: 149 collegamenti a confronti; il numero varia con i feed.
- Ogni scheda include prezzi, formato, costo/kg, disponibilità al rilevamento, date e fonti, avvisi e link commerciali effettivi. Product/AggregateOffer/BreadcrumbList in JSON-LD; offerte non disponibili escluse dal riepilogo dei prezzi disponibili. Quando manca il confronto recente la pagina diventa noindex senza vecchi prezzi e viene tolta dalla sitemap.
- Commit `318172b`: etichette e titoli distinguono le ricette effettive delle varianti; descrizioni includono GTIN. Verifica locale su 149 confronti: zero gruppi di titoli/descrizioni duplicati. Non aggregare varianti con ricetta diversa nelle vecchie pagine editoriali.
- Commit `acb4add`: 404 con ricerca e recupero, noindex, collegamenti assoluti per percorsi annidati. Verifica pubblica su percorso inesistente: HTTP404 e modulo presente.
- Commit `6119ecc`: tre immagini social PNG 1200×630, circa 24–25 KB ciascuna; metadati Open Graph/Twitter applicati dalla pipeline a tutte le pagine indicizzabili, senza attivare email o nuove campagne. File: `automation/apply_social_metadata.py`, `automation/build_social_images.py`, `.github/workflows/catalog.yml`, `site/assets/social-*.png`. Anteprima grafica controllata localmente; tag verificati sul sito con richiesta senza cache.
- Verifiche: 28 test Python superati, precedenti 10 JavaScript ancora invariati; pipeline confronti e pipeline social concluse con successo, deploy Cloudflare confermati. Esempio pubblico controllato: JSON-LD BreadcrumbList e Product, due offerte e prezzi presenti nell'HTML iniziale. [Evidenze](seo-verification-2026-10-20.json).
- Limiti: controlli JSON/coerenza dati locali, non ancora Rich Results Test Google; nessun nuovo Lighthouse, nessuna certificazione WCAG o promessa di indicizzazione. Dati e prezzi rimangono fotografie datate. La cache pubblica può mostrare per breve tempo la versione precedente durante la propagazione.
- Prossime priorità: chiudere le voci SEO ancora aperte sopra; quindi segnalazione errori per offerta, carrello risparmio e storico reale. Non riavviare l'audit o rigenerare una seconda architettura di confronti.


## Sessione 20 ottobre 2026, sitemap e marche
- `automation/build_sitemaps.py` e `tests/test_sitemaps.py`: `/sitemap.xml` ora è un indice di partizioni canoniche per pagine, guide, categorie, prodotti e marche. Esclusi noindex, URL esterni e parametri. L'endpoint registrato in robots/Search Console resta invariato; nuova lettura da Google non ancora verificata.
- `automation/sitemap-state.json` conserva impronta del contenuto significativo e lastmod osservato. Alla prima inventariazione la data storica sconosciuta viene omessa. Aggiornamenti del solo orologio di recupero o copyright non spostano lastmod; prezzi, testo, link nel contenuto e schema modificati sì. Test specifici passati; riferimento: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap .
- `automation/build_brand_pages.py` e `tests/test_brand_pages.py`: cinque landing per Monge, Royal Canin, Farmina, Natural Trainer, Purina Pro Plan, più `/marche`. Richiedono almeno 12 offerte recenti della marca esatta, senza includere automaticamente altre linee. Campione di 24 offerte per pagina con rotazione alfabetica dei negozi, fonte, formato, peso disponibile e data; collegamenti ai confronti GTIN solo quando esistono. Nessuna classifica nutrizionale o selezione per commissioni.
- ItemList e BreadcrumbList corrispondono ai contenuti visibili delle landing. Verifica pubblica `/marca-monge`: HTTP200, 24 schede e 24 elementi ItemList. Sitemap marche pubblica: sei URL. Collegamento alle marche nella home; fonti, strumenti e guide collegati dalle landing. Le pagine con dati insufficienti diventano noindex senza vecchi prezzi.
- `.github/workflows/catalog.yml` genera marche prima della home, metadati social e sitemap alla fine; versiona stato e partizioni. Le due esecuzioni catalogo sono concluse con successo. `site/_headers`: HSTS max-age=86400 verificato su risposta pubblica; senza includeSubDomains o preload. Cache osservata: max-age=0, must-revalidate; compressione non certificata.
- `site/assets/style.css`: titoli delle nuove schede marca a 18px, evitando la tipografia grande della pagina. Nessuna prova browser mobile completa o nuovo Lighthouse in questa sessione.
- Verifiche: 31 test Python e 10 JavaScript della pipeline; idempotenza/lastmod/noindex, identità esatta della marca e rotazione fonti; XML con URL unici e corrispondenza ItemList/schede. [Evidenze](seo-structure-verification-2026-10-20.json).
- Prossimo: completare validazioni tecniche pendenti senza riavviare l'audit, quindi segnalazione errori per prezzo e carrello risparmio; nessun blocco totale, continuare il lavoro autorizzato. Restano invariati i blocchi di credenziali, privacy, nuovi feed e invio email sopra elencati.


## Sessione 20 ottobre 2026, liste e segnalazioni
- Commit `f7ee240`: helper `automation/list_schema.py` e test; ItemList applicato alle tre categorie e agli indici prodotti, confronti GTIN e marche, oltre alle landing marca già complete. Nomi/URL vengono dalle schede e dai collegamenti visibili; nessuna recensione, equivalenza o rating dedotto. Verifica pubblica categoria crocchette cani: 24 elementi. Fonte consultata: https://schema.org/ItemList .
- Commit `e0196fc`: segnalazione errori accanto alle offerte statiche (home, categorie, prodotti, confronti, marche) e dinamiche nel comparatore. File nuovi: `automation/report_link.py`, `site/segnala-errore.html`, `site/assets/report.js`, test Python e Node; aggiornati generatori, home/catalog/trade JS, CSS e workflow.
- `/segnala-errore` prepara nel browser un testo con soli ID offerta, titolo, negozio, prezzo e data riportati nel collegamento. Anteprima prima del link al programma email; l'invio resta un'azione del visitatore. Nessun endpoint di raccolta, iscrizione o invio automatico, nessun indirizzo email dell'utente o URL affiliato nei parametri. Destinatario ripreso dal contatto già pubblicato sul sito. Nessun messaggio inviato durante lo sviluppo.
- Dati del collegamento dichiarati non verificati; nessuno SLA di risposta inventato. Campi accessibili, descrizione massima 1000 caratteri, avvertenza di non inserire dati sanitari/documenti/pagamenti. Pagina noindex e invio disabilitato senza JS, con alternativa email esplicita. La conferma/correzione pubblica di segnalazioni reali richiede ancora gestione del titolare: non inventare ticket.
- Verifiche: 33 test Python e 11 JavaScript, sintassi JS, pipeline e deploy Cloudflare riusciti. Test su allowlist, limiti, escape dei dati e assenza di URL affiliati/identificatori personali nella segnalazione. Modulo pubblico e 24 collegamenti di segnalazione nella categoria verificati; non ancora prova browser manuale completa del modulo o della consegna email.
- Compressione CSS verificata con Accept-Encoding br: Content-Encoding br, 8643 byte nella richiesta osservata; cache public,max-age=0,must-revalidate e HSTS confermati. Nessuna nuova misura Lighthouse né certificazione Rich Results/WCAG. [Evidenze](feedback-and-lists-verification-2026-10-20.json).
- Prossimo lavoro concreto: carrello risparmio locale con totali di spedizione corretti per ordine, e ordinamento del comparatore per totale soltanto dove stimabile. Completare gli altri strumenti e contenuti autorizzati; non ripetere audit, creazione pagine marca o modulo segnalazioni. Persistono i blocchi esterni già descritti; nessun blocco totale.


## Sessione 20 ottobre 2026, lista risparmio e totale per ordine
- Commit `2cb4175`, correzione `ad85037`: `site/assets/basket.js`, `/carrello-risparmio`, pulsanti Aggiungi alla lista nel comparatore, contatore, gestione quantità/rimozione/svuotamento. Conservati nel browser solo ID offerta e quantità (20 prodotti, 10 confezioni per prodotto); niente login, sincronizzazione, ordini o carrelli creati nei negozi.
- Il confronto valuta l'intera lista per ogni negozio: corrispondenza esclusivamente per GTIN valido normalizzato, marca e peso netto; senza codice si usa soltanto l'offerta esatta. Nei negozi con assortimento incompleto non viene mostrato un totale apparentemente conveniente. Per ogni prodotto si sceglie la confezione dal prezzo più basso tra le corrispondenze disponibili; coupon, abbonamenti e supplementi non modellati non sono ottimizzati.
- Spedizione calcolata una volta sul subtotale dell'ordine e sulla somma dei pesi di spedizione per quantità, distinti dal peso netto. Prezzi in centesimi; nessun arrotondamento del peso verso il basso alla soglia dei supplementi. Senza condizioni/peso verificabili, con prezzi scaduti, destinazioni speciali o offerte mancanti il totale resta non disponibile.
- Fonti ufficiali delle tre condizioni riverificate il 20 ottobre e `shipping-rules.json` aggiornato: WebPet gratuito da 39,90 €; Bauzaar oltre 59 € e fino a 35 kg, con soglia esatta 59 € non chiarita; Animaliapet ancora discordante. Non estendere automaticamente tariffe a servizi/località esclusi e non inventare supplementi.
- `catalog.js`/HTML: ordine iniziale per totale stimato (anche sulle offerte), dati non stimabili in coda con avviso; gruppi coerenti con la scelta dell'ordinamento. Cache delle quote per ciascun rendering e indice del carrello per evitare calcoli ripetuti sul catalogo. Nessun ordinamento per commissioni.
- Verifiche locali: 33 test Python e 18 Node. Casi di soglia aggregata, centesimi, assortimento parziale, ricetta/formato diverso, pesi ignoti/scaduti, disponibilità, lista manomessa, ID rimosso e peso 35,004 kg che non deve diventare 35 kg. Pipeline cataloghi conclusa con successo.
- Nuovo controllo CI mobile isolato, `.github/workflows/basket-browser.yml` + `tests/check_basket_browser.mjs`: Chrome reale a 393×852, file locali, rete esterna bloccata e orologio sul generated_at del campione (non metriche sul campo). Aggiunta dal comparatore, default totale, quantità conservata al reload, ID rimosso senza totale, zero errori JS e zero overflow orizzontale passati. Screenshot esaminato. Esito browser: https://github.com/offerte4zampe/zampachiara/actions/runs/39364031777 ; guardia finale con test Node e browser riuscita: https://github.com/offerte4zampe/zampachiara/actions/runs/39364214662 . Artefatti screenshot disponibili per 14 giorni; [sintesi persistente](../audits/2026-10-20/basket-browser-summary.json).
- Deploy Cloudflare verificati; pagina pubblica disponibile e noindex, script presente. Nessun invio email o clic affiliato eseguito nei test. Nessun nuovo Lighthouse né prova CrUX. [Evidenze](basket-verification-2026-10-20.json).
- Prossimo lavoro concreto: storico osservato e calcolatore costo giornaliero nelle schede; poi qualità dei dati e preparazione degli alert senza raccolta email fino ai requisiti verificati. Non ricreare carrello o audit. Persistono i blocchi esterni riportati sopra; non dichiarare completamento totale.


## Sessione 20 ottobre 2026, costo giornaliero nelle schede
- `site/assets/daily-cost.js`: calcolo con razione manuale in grammi, senza valori preimpostati o raccomandazioni nutrizionali. Prezzo/peso netto × grammi/1000, costo per 30 giorni; spedizione esclusa e rilevazione non in tempo reale espliciti. Nessuna raccolta o salvataggio della razione.
- Integrato nelle schede e gruppi del comparatore e nel generatore delle pagine prodotto GTIN. Senza peso netto, disponibilità, prezzo recente valido o razione positiva non viene mostrata una stima. Il peso di spedizione non entra nel calcolo. Input etichettato e risultato annunciato, controlli con area di almeno 44px.
- Test locali: 33 Python e 21 Node superati, inclusi tre casi specifici su formula, precisione delle piccole porzioni, dati scaduti/futuri/incompleti e assenza di razioni predefinite. Estesa prova browser mobile isolata alla compilazione manuale; pipeline/deploy da verificare dopo il commit. Nessun nuovo Lighthouse o dato di salute verificato.
- Prossimo: verificare pipeline e browser, quindi storico osservato 30/90/180 giorni e qualità dei dati. I blocchi esterni sopra restano invariati; lavoro complessivo non concluso.
