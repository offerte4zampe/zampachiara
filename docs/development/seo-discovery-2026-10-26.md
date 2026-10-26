# Migliore scoperta delle pagine — 26 ottobre 2026

## Problema verificato
Search Console mostra 56 URL indicizzati e molte pagine utili non ancora scansionate. Menu Guide punta a scelte (pagina risorse), la home rinvia soprattutto al comparatore parametrico, molti collegamenti statici transitano da alias .html che reindirizzano. Non è una penalizzazione dimostrata e non si rimuovono noindex di moduli, carrello o confronti senza dati.

## Modifiche
- Generatore finale improve_discovery.py legge le canonical dei file realmente presenti. Normalizza soltanto gli anchor locali noti, conserva query e frammenti, non modifica URL commerciali, dati, robots, canonical dichiarate o prezzi. Endpoint prodotto dinamico e download conservati.
- Guide nel menu porta al vero indice guide-risparmio. Footer collega guide, marche e confronti per prodotto.
- Home: sei guide pratiche con link HTML diretti e descrittivi; marche curate puntano alle pagine di marca soltanto se indicizzabili. Hydration mantiene le destinazioni dichiarate dal documento.
- Idempotenza del menu Preferiti e collegamento Marche corretta per convivere con URL canoniche già normalizzate.
- Report data/discovery.json misura grafo dei link fra pagine indicizzabili, raggiungibilità dalla home e profondità massima; tiene conto degli alias prima del confronto per non attribuire falsi miglioramenti.
- Pipeline catalogo e CI browser applicano il passaggio dopo i generatori e prima di sitemap/audit. Server della prova browser gestisce URL senza estensione come Workers Assets; prova guida collegata dalla home e link diretti verificati.
- Fonti: https://developers.google.com/search/docs/crawling-indexing/links-crawlable e https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls consultate il26ottobre2026.

## Verifica
99 test Python e78 Node locali superati. Test sintentici preservano query, frammenti, affiliati e noindex, controllano idempotenza e miglioramento della profondità su fixture. CI, generazione completa e produzione da verificare. Nessuna promessa sui tempi o sulle decisioni d’indicizzazione di Google. Nessuna richiesta AdSense inviata.
