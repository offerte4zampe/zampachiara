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
1. Completare SEO: pagine marca utili, ItemList sulle liste, sitemap per tipo con lastmod basato su cambiamenti reali; validazione Google Rich Results ancora da eseguire. Home e confronti GTIN sono già prerenderizzati.
2. Verificare cache/header e accessibilità mobile delle nuove pagine. 404 e metadati social già implementati; niente migrazioni URL inutili.
3. Copertura matching e peso netto; correzioni prezzo, carrello browser, storico reale, costo giornaliero manuale dove manca razione ufficiale.
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
