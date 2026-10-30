# Task 13 — consenso, link commerciali e AdSense

Tutti i link /go/ e i collegamenti riconosciuti come affiliati mantengono l'href esatto e includono sponsored, nofollow e noopener (oltre a noreferrer). Le risposte /go/, incluse quelle di fallback, hanno X-Robots-Tag: noindex, nofollow e restano no-store. robots.txt già vietava /go/: conservato.

Il meta google-adsense-account viene rimosso insieme al loader AdSense: manca una CMP certificata verificata. Anche il caricamento automatico delle campagne rimane disabilitato, senza richieste di configurazione, script o immagini pubblicitarie; gli spazi editoriali locali per le collaborazioni restano disponibili. La configurazione attuale non aveva campagne attive.

Le statistiche facoltative e le preferenze salvate non cambiano. I test esistenti verificano richieste /api/metrics soltanto dopo opt-in e rispetto di GPC/DNT; il browser smoke ora registra le richieste metrics e richiede zero chiamate prima del consenso. I redirect affiliati funzionano senza consenso e preservano integralmente le destinazioni.

Validazione: 201 test Python, 150 Node; idempotenza e integrità degli href, assenza di meta/loader, nessuna richiesta automatica di annunci, consenso e header outbound; audit statico e Wrangler dry-run. File: automation/remove_unverified_ads.py, Worker outbound/canonico, client product/advertising, hook build/workflow e test dedicati. D1/shadow e regole di spedizione invariati.
