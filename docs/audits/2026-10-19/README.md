# Offerte a 4 Zampe — audit iniziale, 19 ottobre 2026

## Esito e priorità

Prima di ampliare la grafica, correggere la stabilità del comparatore mobile e il caricamento della home. La guida è già veloce nello stesso ambiente: il problema non riguarda uniformemente tutto il sito. Questa consegna documenta la baseline; non include ancora modifiche al prodotto né risultati «dopo».

## Metodo e riproducibilità

Codice/catalogo analizzati: commit `6158602e3115503a0302e131e6433c52e84d6362`. Rilevazione statica alle 20:11 UTC; catalogo generato alle 20:02 UTC del 19 ottobre. Controllati 25 documenti di contenuto, un file di verifica Google e 15 URL pubblici.

Lighthouse 13.5.0, profilo mobile, una esecuzione sintetica per pagina, circa 20:12–20:13 UTC. [Esecuzione GitHub Actions](https://github.com/offerte4zampe/zampachiara/actions/runs/39317381066); workflow `.github/workflows/site-audit.yml`, avviabile manualmente. I report completi JSON/HTML sono nell'artefatto `public-site-mobile-audit`, conservato fino al 2 novembre 2026. Sintesi, dettagli e immagini qui restano versionati. PageSpeed API aveva risposto 429: le misure sotto provengono dalla successiva esecuzione Actions riuscita.

| Pagina | Performance | Accessibilità | Best practices | SEO | LCP | CLS | TBT |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Home | 55 | 95 | 58 | 100 | 11,9 s | 0 | 356 ms |
| `/confronta-cibo` | 39 | 97 | 58 | 100 | 7,1 s | 1,008 | 66 ms |
| `/costo-crocchette-cane` | 99 | 95 | 81 | 100 | 1,7 s | 0 | 104 ms |

Sono misure di laboratorio, variabili con rete e terze parti. TBT non è INP; questo test di caricamento non misura INP reale. SEO 100 non dimostra indicizzazione o posizionamento. Nessuna certificazione Core Web Vitals deriva da una singola esecuzione.

## Prestazioni e interfaccia

Il nodo LCP è il titolo nella home e il paragrafo introduttivo nel comparatore: non un'immagine prodotto. Sul comparatore Lighthouse attribuisce gli spostamenti a `body` (circa 1) e `#catalog-filters` (0,0078). La causa va isolata con esperimenti su caricamento catalogo, CSS e pubblicità, senza attribuirla a priori a uno solo.

Home e comparatore trasferiscono rispettivamente circa 1.771 e 1.596 KiB; la guida circa 46 KiB. Il catalogo completo pesa 1.263.170 byte compresso e 11.648.743 decodificato. Servire alla home un sottoinsieme prerenderizzato e caricare progressivamente il resto è un candidato concreto. Il CSS trasferito è compresso: i controlli HTTP con `Accept-Encoding: identity` non indicano assenza di compressione.

Lighthouse rileva JavaScript inutilizzato e il cookie DoubleClick `test_cookie` su home/comparatore. Serve una prova separata del comportamento di consenso in area SEE; il runner non aveva geolocalizzazione SEE verificata. Questo rilievo tecnico non costituisce un giudizio legale né prova approvazione AdSense.

## Accessibilità

Il colore primario `#267c76` su bianco passa AA per testo normale (4,97:1). I problemi emergono su sfondi colorati effettivi:

| Elemento | Colori testo / fondo | Contrasto |
| --- | --- | ---: |
| Home e comparatore, `.kicker` | `#ad563b` / `#eaf3ed` | 4,44:1 |
| Home, descrizioni/stato/microtesto | `#637577` / `#eaf3ed` | 4,27:1 |
| Home, paragrafo newsletter | `#5f716b` / `#ffead0` | 4,41:1 |
| Guida, richiamo finale `.kicker` | `#ad563b` / `#ffe8cb` | 4,23:1 |
| Guida, richiamo finale paragrafo | `#637577` / `#ffe8cb` | 4,06:1 |

Correggere questi abbinamenti verso almeno 4,5:1 per testo normale. La scheda dinamica della home salta a un `h3` senza precedente `h2`. Ogni pagina di contenuto ha un H1; nessun alt mancante o controllo privo di etichetta emerge dalla sola scansione statica. Il collegamento «Vai al contenuto» riceve focus con Tab e raggiunge `#main`. Restano da verificare interazione completa da tastiera, lettore schermo, zoom 200% e tabella larga su mobile. È presente la gestione `prefers-reduced-motion`.

## Rendering, SEO e contenuti

Home e comparatore non espongono prezzi nel documento HTML iniziale e caricano le schede via JavaScript. Le pagine categoria/prodotto esaminate contengono già prezzi statici. Google può renderizzare JavaScript, ma HTML utile iniziale riduce dipendenze e migliora esperienza e verificabilità.

Nessun titolo, descrizione o canonical duplicato rilevato; nessun collegamento interno rotto nella scansione statica. Le varianti filtro del comparatore hanno già canonical verso `/confronta-cibo`: non applicare automaticamente altre direttive senza definire quali landing debbano essere indicizzate. Sitemap pubblica: 23 URL. Search Console è già presente, sitemap accettata; elaborazione/metriche ancora insufficienti e nessun dato Core Web Vitals utilizzabile. Non si può dedurre traffico odierno o numero attuale di pagine indicizzate.

`/index.html` e `/confronta-cibo.html` restituiscono 307 verso gli URL puliti: valutare 301/308 se la migrazione è permanente. Un percorso inesistente restituisce correttamente 404; manca una pagina di recupero utile. Il prodotto Monge non più disponibile è intenzionalmente `noindex,follow`, fuori sitemap: non è una landing da riempire artificialmente. Usare `lastmod` coerenti con modifiche reali del contenuto.

Schema rilevato: WebSite, Organization e Article; mancano Product, AggregateOffer e BreadcrumbList. Introdurli solo dove i dati sono visibili e attendibili. AggregateOffer deve riferirsi allo stesso prodotto, non riunire ricette o formati diversi. Non promettere rich result FAQ o casella di ricerca: Google li ha ritirati. Le parole chiave/intenti nel CSV sono proposte editoriali, non volumi misurati; il conteggio delle occorrenze monetarie non è un conteggio offerte.

## Qualità e copertura del catalogo

- 13.186 offerte, 12.497 disponibili: Bauzaar 7.174, WebPet 2.020, Animaliapet 3.992.
- GTIN valido per 6.989 offerte; peso netto per 3.853 (29,2%).
- 126 gruppi confrontabili tra negozi, 252 offerte (1,91% del catalogo). La dimensione complessiva non equivale a copertura di confronto.
- Confronto rigoroso per GTIN, marca e peso esplicito; non allentare le regole per aumentare artificialmente i risultati.
- 7.147 pesi di spedizione Bauzaar: distinti dal peso netto, non usarli per €/kg.
- Nessun conflitto nella verifica euristica limitata dei titoli «n × peso»; non prova correttezza universale.
- Nessun recupero oltre 36 ore nella fotografia. L'età misura il recupero: il feed Bauzaar è giornaliero e non espone `upstream_last_modified`. Non equivale all'età effettiva del prezzo presso il negozio.

Bauzaar è l'affiliazione effettivamente attiva in questo catalogo. Non presentare Amazon o altri negozi come integrazioni operative senza dati e accessi verificati. Mantenere informativa commerciale leggibile e ordinamento indipendente dalle commissioni.

## Retention e misurazione

La configurazione newsletter non ha ancora URL di iscrizione attivo; doppio consenso e disiscrizione non risultano verificati. Prima del lancio completare dati del titolare nell'informativa e prova end-to-end Brevo, senza inventare identità o promettere codici esclusivi. Nessuna email inviata o lista iscritti consultata per questo audit.

Il lettore analytics Cloudflare esiste, ma credenziali/zone ID non sono disponibili in questo runtime. Non è dimostrato un reporting API operativo. Gli eventi interni consensuali non equivalgono a persone uniche o vendite.

## Prossimi interventi, in ordine

| Priorità | Intervento | Impatto / impegno | Verifica e rischio |
| --- | --- | --- | --- |
| P0 | Stabilizzare comparatore: riservare spazio e isolare inserimenti tardivi in HTML/CSS/JS | Alto / medio | Ripetere 3 prove mobile, confrontare CLS e video; preservare filtri e risultati |
| P0 | Ridurre lavoro iniziale home/catalogo; sottoinsieme statico e caricamento progressivo | Alto / medio-alto | LCP e byte prima/dopo; mantenere corrispondenza dati e freschezza |
| P1 | Correggere contrasti e gerarchia titolo scheda home | Medio / basso | Audit automatico più tastiera/zoom, senza cambiare identità grafica |
| P1 | Product/AggregateOffer/BreadcrumbList sulle pagine idonee | Medio / medio | Validazione schema, prezzi visibili identici, esclusione prodotti scaduti |
| P1 | Ampliare peso netto e matching sicuro, poi nuovi feed autorizzati | Alto / medio-alto | Copertura e controlli varianti; niente equivalenze approssimative |
| P1 | Completare privacy, prove Brevo e misurazione autorizzata | Alto / dipendenze esterne | Iscrizione/conferma/disiscrizione reali, report API verificato |
| P2 | 404 utile, redirect permanenti, landing con domanda verificata | Medio / basso-medio | Status/canonical, contenuto specifico; evitare pagine vuote in serie |

Separare gli interventi in commit piccoli. Dopo ogni modifica alle prestazioni confrontare almeno tre esecuzioni nello stesso ambiente e verificare funzionalità reali; non riutilizzare questa baseline come risultato successivo.

## Evidenze

[Inventario pagine](pages.csv) · [Baseline statica/catalogo](baseline.json) · [HTTP](http-checks.json) · [Lighthouse sintesi](lighthouse-summary.json) · [Lighthouse dettagli e selettori](lighthouse-details.json) · [Verifica euristica pesi](weight-review-candidates.json).

[Home mobile](home-mobile.jpg) · [Comparatore mobile](confronta-cibo-mobile.jpg) · [Guida mobile](costo-crocchette-cane-mobile.jpg).

## Riferimenti primari consultati

- [Lighthouse](https://developer.chrome.com/docs/lighthouse/overview)
- [Core Web Vitals](https://web.dev/articles/vitals)
- [WCAG: contrasto minimo](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
- [Google: JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics)
- [Google: Product e AggregateOffer](https://developers.google.com/search/docs/appearance/structured-data/product-snippet)
- [Aggiornamenti documentazione Search](https://developers.google.com/search/updates)
- [Ritiro sitelinks search box](https://developers.google.com/search/blog/2024/10/sitelinks-search-box)
