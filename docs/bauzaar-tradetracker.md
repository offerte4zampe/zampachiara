# Bauzaar / TradeTracker

Verificato il 19 ottobre 2026: campagna 16143 accettata per il sito 518044.
Feed standard 600171: 7.174 prodotti al controllo, aggiornamento dichiarato giornaliero.
Il feed CSS 2203612 non viene usato.

Il job del catalogo consulta il feed ogni sei ore; questa frequenza non aumenta quella del fornitore. checked_at indica il recupero del feed, non una verifica del checkout. Un errore conserva le osservazioni precedenti con le date originali. Una risposta valida sostituisce interamente Bauzaar, rimuovendo le offerte non più presenti.

URL pubblico del feed, senza password o token: definito in automation/bauzaar_feed.py. Non aggiungere esportazioni grezze al repository.

Ogni destinazione deve essere una variante Shopify esplicita su www.bauzaar.it. L'URL commerciale originale fornito dal feed è conservato separatamente dall'URL diretto. I pesi provengono solo da unit_pricing_measure in kg/g; litri e conteggi non diventano kg. Non si importano coupon dai titoli o sconti percentuali dal prezzo di riferimento. Un sale_price vale solo nel periodo esplicitamente indicato. I GTIN sono sottoposti al checksum nell'arricchimento. I dati ufficiali non vengono sovrascritti dalla cache dello scraping.

Commissioni segmento Generale: 8% brand esclusivi, 6% nuovi clienti, 1,6% clienti esistenti. Cookie 30 giorni. Annullamenti e resi possono causare rifiuti; non sono ricavi garantiti.

SEM vietato. Le anteprime DEM/newsletter promozionali richiedono approvazione preventiva dell'inserzionista tramite account manager. Non inviare la newsletter archiviata automaticamente e non sostituirne i link con affiliati senza questa approvazione.
