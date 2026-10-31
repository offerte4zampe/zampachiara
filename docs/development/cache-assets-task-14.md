# Task 14 — cache e asset con hash

La build produce 42 asset con hash del contenuto nel nome. Le dipendenze locali (compresi Worker e immagini CSS) sono riscritte prima del calcolo dell'hash del file che le usa. HTML e metadati social puntano ai file verificati; gli originali rimangono disponibili. Gli URL esterni, inclusi quelli affiliati, non vengono riscritti. Un passaggio di ripristino permette build ripetute senza duplicare script o accumulare riferimenti obsoleti.

Gli asset con hash hanno Cache-Control: public, max-age=31536000, immutable tramite regole esatte in _headers; i dati hanno max-age=60 e stale-while-revalidate=300. Le immagini prodotto eventualmente autorizzate usano il percorso locale già stabile. Le intestazioni di sicurezza preesistenti restano intatte. Manifest e file con hash sono generati, non nuove copie sorgente da mantenere manualmente.

Gli script esterni privi di async/defer ricevono defer; il browser smoke controlla l'assenza di script bloccanti nell'head e i flussi completi dopo il fingerprint. Il Worker elimina il resolver legacy anche quando il nome è hashato. Il sito usa font di sistema e non scarica file font: font-display e preload di un font esterno non sono applicabili.

Verifiche locali: 202 test Python, 151 Node; hash e dipendenze, URL commerciali intatti, idempotenza, ripristino, Cache-Control e schema canonico; audit statico e Wrangler dry-run. Controllo dei file generati: zero asset locali mancanti e zero script duplicati.

Verifiche di produzione da completare dopo il merge: header degli asset e dei dati, ETag, negoziazione Brotli per JSON non già gzip, PageSpeed mobile su home, comparatore e scheda. Non viene forzata una seconda compressione sui cataloghi .json.gz. Baseline e misura intermedia sono in docs/audits/2026-10-30. INP resta misurabile soltanto se CrUX dispone di dati; TBT non viene presentato come INP.

File: automation/fingerprint_assets.py, hook Wrangler e workflow layout/browser, compatibilità del Worker canonico e test dedicati. Prezzi, link affiliati, consenso, D1/shadow e regole di spedizione invariati.
