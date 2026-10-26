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
- Fonti: https://developers.google.com/search/docs/crawling-indexing/links-crawlable e https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls consultate il 26 ottobre 2026.

## Verifica conclusa
- Commit funzionale 1c0f1c9fc31d49ca79f97e4fb74602169ab61c8f.
- 99 test Python e 78 Node superati localmente e nella CI mobile 40334912704. Test sintetici controllano conservazione di query, frammenti, affiliati e noindex, idempotenza e profondità su fixture. Controllo browser mobile riuscito, incluso clic sulla guida lettiere dalla home.
- Rigenerazione catalogo 40334912752 riuscita; commit generato 0b45d634e040edd7a1ce6fffd1d54e542192fc9b pubblicato con Cloudflare Workers Builds success (check 121614974263).
- Report reale: 466 pagine, 326 indicizzabili, tutte raggiungibili dalla home, zero pagine isolate, profondità massima 2. La profondità massima era già 2 prima del passaggio: nessuna riduzione globale o risoluzione di pagine isolate attribuita a questa modifica.
- Produzione osservata: sei schede guide e collegamenti alle marche presenti; clic dalla home apre https://offerte4zampe.it/confrontare-prezzi-lettiere con il contenuto atteso.
- Nessuna promessa sui tempi o sulle decisioni d’indicizzazione di Google. Nessuna richiesta di indicizzazione Search Console o nuova revisione AdSense inviata.
