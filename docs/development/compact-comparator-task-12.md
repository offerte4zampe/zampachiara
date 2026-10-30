# Task 12 — comparatore più compatto

Il calcolatore manuale A/B è nella pagina Budget (`/calcolatore#manual-tool`), con gli stessi campi, formule, marker testuali e controlli. Il pulsante Usa come A/B apre Budget con le offerte selezionate nel frammento, senza inventare razioni o costi di spedizione. I vecchi link condivisi con `#v=1` vengono trasferiti dal client conservando i valori. Il budget annuale esistente e i piccoli strumenti per singola offerta rimangono disponibili.

Nel comparatore la ricerca viene prima dei testi di metodo; i filtri avanzati sono espandibili. Stima spedizione e condivisione restano nella pagina, dopo i risultati. I testi didattici sono abbreviati e collegano guida e calcolatore. La ricerca, l'ordinamento, le faccette, la selezione e i calcoli di spedizione non cambiano.

Verifiche: 200 test Python e 149 Node; trasformazione idempotente, nessun campo A/B o food.js nel comparatore, stessi campi e script in Budget; audit statico e build Wrangler riusciti. Il browser smoke verifica il calcolo A/B in Budget, i filtri espandibili e il primo risultato a meno di 700px in viewport mobile 393×852, oltre ai flussi precedenti di confronto, lista e condivisione.

File: automation/apply_compact_comparator.py e partial manual-food.html, client catalog/food/base, CSS, hook build/workflow e test. La migrazione è applicata alla build, senza duplicare sorgenti HTML generati. Destinazioni affiliate, preferenze di tracking, D1/shadow e regole di spedizione invariati.
