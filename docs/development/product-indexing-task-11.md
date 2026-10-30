# Task 11 — indicizzazione e metadati social

Regola documentata nel Worker e nel modello: pagina indicizzabile con almeno due negozi distinti che offrono lo stesso prodotto con quantità verificata, oppure almeno 30 date con osservazioni effettive valide. Le date duplicate, future e non valide non aumentano il conteggio. Una coppia di offerte dello stesso negozio non vale due negozi. La soglia dello storico si applica anche agli archivi con dati reali conservati; gli archivi che reindirizzano non entrano nella sitemap.

Il Worker ricalcola la regola con disponibilità, scadenze delle revisioni e freschezza delle offerte. Parametri quantità o territorio diversi dalla vista canonica rimangono noindex. Meta robots e X-Robots-Tag concordano. Product/AggregateOffer vengono emessi soltanto sulla vista indicizzabile; prezzi e disponibilità derivano dalle stesse righe mostrate nella tabella, senza riempire le spedizioni sconosciute.

og:image e twitter:image adottano l'immagine locale del prodotto soltanto con percorso valido e asset realmente esistente; il Product schema usa allora la medesima immagine. Se manca, resta il social visual locale generico. Al momento non sono state verificate licenze di cache dei cinque negozi (Task 6): nessuna nuova immagine è scaricata e il requisito di un'immagine prodotto locale per ogni scheda resta subordinato ai permessi.

Verifiche: 199 test Python e 149 Node, soglie 29/30 date, negozi distinti, archivi con storico, viste con parametri, schema assente nelle pagine noindex, prezzi coerenti e asset locale presente/mancante. Build Wrangler e audit statico superati. Le sitemap seguono la stessa regola al successivo aggiornamento del modello.

File: automation/build_product_catalog.py, worker/canonical-product.mjs, test prodotto esistenti aggiornati alla nuova regola e nuovi test di indicizzazione. Nessuna modifica a identità, slug, link affiliati, preferenze di tracking, D1/shadow o regole di spedizione.
