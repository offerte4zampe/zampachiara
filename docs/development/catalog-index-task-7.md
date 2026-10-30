# Task 7 — indice del comparatore

Il comparatore mantiene 24 gruppi prodotto prerenderizzati in build, disponibili senza JavaScript. Cloudflare serve questo HTML tramite il binding degli asset: non serve un rendering per richiesta del medesimo snapshot. L'indice viene caricato alla prima interazione o quando un URL richiede filtri; la prima vista conserva i risultati HTML.

`automation/build_catalog_index.py` genera un manifest e shard gzip da massimo 1.000 offerte, ordinati per marca e ID. I nomi dipendono dal contenuto. Restano disponibili anche gli shard della generazione precedente. Il client scarica al massimo tre shard contemporaneamente e li decodifica in Worker; il fallback riutilizza gli stessi Blob. Non richiede `catalog.json.gz` nel comparatore. Gli altri strumenti mantengono il loro caricamento completo.

L'indice contiene i campi effettivamente necessari per ricerca, confronto, strumenti personali e spedizione. Non contiene URL commerciali né campi di provenienza del feed. Lo snapshot completo e i suoi link affiliati rimangono intatti; le card aprono lo slug canonico e i dettagli commerciali risiedono nella scheda. L'ordine originale viene ripristinato prima del ranking per conservare gli spareggi.

Con oltre 5.000 righe un Worker persistente filtra testo, negozio, marca, disponibilità e faccette. Il thread principale mantiene le formule originali di spedizione e ordinamento. Errori o timeout del Worker tornano al filtro esistente; risposte superate non aggiornano la pagina. Debounce ricerca: 150 ms. Griglia e anteprima riservano almeno 60vh.

Misure snapshot 30/10/2026: 16.691 offerte, 17 shard, 1.654.241 byte gzip contro 2.113.070 del catalogo completo (−21,7%). La granularità riduce la dimensione di ogni parse; il totale rimane significativo perché conserviamo le verifiche di identità e spedizione.

Verifiche: 192 test Python; 141 test Node; test specifico su tutte le offerte per equivalenza ricerca, faccette, raggruppamenti e spedizione con quantità 1/3/10; audit statico 499 pagine; build Wrangler dry-run. Il browser smoke misura zero download del catalogo completo e un download per shard.

Baseline PageSpeed mobile prima dei Task 6/7: home 98, LCP 906ms, CLS 0, TBT 0; scheda 99, LCP 1960ms, CLS 0, TBT 0; comparatore 100, LCP 905ms, CLS 0, TBT 0. Report in `docs/audits/2026-10-30/before-task-6-7.json`. INP non disponibile per assenza di dati CrUX: TBT non è una misura di INP. La misura dopo la pubblicazione resta da effettuare, senza presentare la baseline come risultato della modifica.
