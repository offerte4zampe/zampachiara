# Primo intervento sulle prestazioni — 19 ottobre 2026

Implementazione: `9e3c3364431430152e3bd21809129e96b5883d6a`.

La home carica ora `data/home.json`: 8.944 byte nella prima generazione, rispetto ai 1.263.170 byte del catalogo compresso precedente (99,29% in meno per quel download). Il documento contiene solo candidati alle offerte, statistiche complessive e marche principali; i prezzi sono copiati senza alterazioni. Il comparatore continua a usare il catalogo completo.

`automation/build_home_data.py` viene eseguito al termine di ogni aggiornamento del catalogo. Il selettore esclude dati oltre 36 ore, indisponibili e prezzi di riferimento fuori dalla soglia già usata dal sito. Restano le avvertenze sulla disponibilità e sulla conferma del prezzo nel negozio.

I messaggi asincroni del comparatore hanno spazio riservato per ridurre gli spostamenti dei filtri. Corretti i contrasti del testo su sfondi colorati e la gerarchia del titolo della scheda in evidenza nella home.

## Controlli

25 test Python e 10 test JavaScript superati; sintassi home.js e diff verificati. Confrontati tutti i campi delle 15 offerte nel payload con la fotografia del catalogo: coincidono. Il nuovo file è stato verificato anche all'URL pubblico dopo il deploy Cloudflare riuscito.

## Misura mobile

[Tre prove per pagina](https://github.com/offerte4zampe/zampachiara/actions/runs/39320468707), stessa versione Lighthouse 13.5.0 della baseline. La baseline precedente aveva una sola prova per pagina: il confronto è indicativo, non un esperimento controllato. I risultati sintetici non misurano INP degli utenti e non sostituiscono dati sul campo. Nel primo audit lo script di controllo Cloudflare aveva un costo CPU rilevante, da considerare insieme a rete e terze parti quando si interpretano i tempi.


| Pagina | Performance prima (1 prova) | Performance dopo (mediana; intervallo) | LCP prima → dopo (mediana) | CLS dopo, 3 prove |
| --- | ---: | ---: | ---: | ---: |
| Home | 55 | 97; 66–99 | 11,90 → 2,35 s | 0 / 0 / 0 |
| Comparatore | 39 | 86; 81–88 | 7,06 → 2,34 s | 0 / 0 / 0 |
| Guida costo crocchette | 99 | 99; 99–99 | 1,70 → 1,71 s | 0 / 0 / 0 |

Il CLS del comparatore era 1,008 nella baseline. Le nuove tre prove non riproducono quello spostamento; la variabilità dei servizi esterni impedisce di attribuire tutto il miglioramento a una sola modifica. LCP home dopo: 1,72–2,68 s; comparatore: 2,33–2,38 s. La prima prova home ha ancora attività bloccante rilevante: conserviamo l'intervallo invece di mostrare soltanto il risultato migliore.

Accessibilità automatica: 100/100 per tutte e nove le esecuzioni, rispetto a 95/97/95 della baseline. Non è una certificazione WCAG. Best practices restano 58 per home/comparatore e 81 per la guida: terze parti/cookie e avvisi browser richiedono ancora un intervento separato. Il punteggio SEO automatico resta 100 e non indica ranking o traffico.

La home trasferisce circa 551–552 KB complessivi nel nuovo audit, contro 1,81 MB nella prima prova precedente. Questi totali comprendono immagini e servizi esterni, non solo il catalogo.

[Metriche delle nove esecuzioni e controlli non superati](lighthouse-after-summary.json). Report completi JSON/HTML nell'artefatto dell'esecuzione, fino al 2 novembre 2026.
