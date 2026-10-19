# Avanzamento roadmap

Ultimo aggiornamento: 19 ottobre 2026.

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
1. Prerendering offerte home, pagine marca/prodotto utili, schema Product/Offer/AggregateOffer/BreadcrumbList; validare dati e render.
2. 404 utile, metadati social, cache/header e link interni senza migrazioni URL inutili.
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
