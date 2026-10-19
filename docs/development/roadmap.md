0. Premesse e regole non negoziabili
Nessuno può garantire posizioni in classifica. L'IA deve lavorare su ciò che è controllabile (qualità tecnica, utilità, contenuti, fiducia) e misurare i risultati.
Regole che l'IA deve rispettare sempre:
• Mai inventare dati. Prezzi, disponibilità, recensioni, test, statistiche e citazioni devono provenire da feed, cataloghi o fonti verificabili e riportare data di rilevamento. Se un dato manca, si mostra come non disponibile.
• Niente recensioni o testimonianze false, niente testi generati in massa senza valore, niente cloaking, link a pagamento non dichiarati, reti di siti. Sono pratiche che portano a penalizzazioni.
• Trasparenza sull'affiliazione: i link affiliati restano segnalati (rel="sponsored" dove opportuno) e l'ordinamento dei risultati non deve dipendere dalle commissioni.
• Salute animale = tema delicato. Nessun consiglio medico o dietetico dichiarato come certo; rimandare al veterinario. Ogni guida con contenuto nutrizionale cita le fonti.
• Conformità: cookie e consenso (GDPR, Garante privacy), informativa privacy aggiornata, regole dei programmi affiliati (Amazon Associates, TradeTracker), AdSense. Per gli sconti, verificare la normativa italiana sulle indicazioni di prezzo e di riduzione (direttiva Omnibus) prima di mostrare percentuali di sconto: preferire il confronto tra negozi al «prima/dopo» dichiarato dal negozio.
• Ogni modifica è piccola, tracciata (commit chiari) e reversibile. Prima di cambiare, misurare lo stato di partenza.
1. Fase 1 — Audit iniziale (giorni 1-3)
Produrre un report con evidenze (screenshot, metriche, URL) su:
1. Rendering e indicizzazione. Le offerte e i risultati si caricano via JavaScript? Controllare cosa vede Google: HTML renderizzato, robots.txt, sitemap.xml, canonical, parametri URL (?q=, ?sale=, ?shop=) che generano duplicati o pagine vuote, stato 200/404/redirect, noindex involontari.
2. Performance. Lighthouse e PageSpeed su mobile per home, comparatore, una guida: LCP, INP, CLS, peso JS/CSS, immagini, font. Obiettivo: LCP sotto 2,5 s, INP sotto 200 ms, CLS sotto 0,1 su connessione mobile.
3. Accessibilità (WCAG 2.2 AA): contrasto del verde #267c76 con testo bianco e grigi, focus visibile, etichette dei campi, navigazione da tastiera, testi alternativi.
4. Contenuti. Elenco di tutte le pagine con parola chiave principale, intento di ricerca, lunghezza, duplicazioni, pagine sottili (pochi contenuti utili).
5. Dati. Copertura catalogo: quanti prodotti, quante marche, quanti con codice EAN/GTIN, quanti presenti in più negozi, età media del dato, errori di parsing del peso/kg.
6. Analytics. Verificare che esistano Search Console e uno strumento di misura rispettoso della privacy (ad esempio Plausible, Matomo o GA4 con consenso). Se mancano, configurarli come primo passo.
Consegna: documento di audit con priorità (impatto alto/medio/basso, sforzo alto/medio/basso).
2. Fase 2 — SEO tecnica (settimane 1-2)
1. Contenuto visibile senza JavaScript. Pre-renderizzare (SSG/SSR) le pagine di categoria, marca e prodotto, così che titoli, prezzi e tabelle siano nell'HTML iniziale. La home non deve mostrare «Caricamento…» a un crawler.
2. URL puliti e stabili, ad esempio /crocchette-cani/royal-canin/, /prodotto/<slug>-<ean>/. Le combinazioni di filtri senza valore SEO: noindex,follow o canonical alla pagina principale.
3. Sitemap XML generata automaticamente, con lastmod reale, divisa per tipo (guide, categorie, marche, prodotti). Inviarla in Search Console.
4. Dati strutturati (schema.org): WebSite con SearchAction, Organization, BreadcrumbList, ItemList per le liste, Product con AggregateOffer/Offer (prezzo, valuta, disponibilità, data) per le schede prodotto, FAQPage dove le FAQ sono realmente visibili, Article con autore e data per le guide. Validare con il Rich Results Test.
5. Title e meta description unici e orientati all'intento (es. «Royal Canin Medium Adult 15 kg: prezzi a confronto e costo al kg»). Un solo H1 per pagina, gerarchia H2/H3 coerente.
6. Link interni: breadcrumb, blocchi «Marche correlate», «Altre taglie», «Guide utili», collegando guide e comparatore in entrambe le direzioni.
7. Open Graph e anteprime social con immagini dedicate per le pagine principali.
8. HTTPS, HSTS, compressione Brotli, cache HTTP, preload dei font critici, pagina 404 utile con ricerca.
3. Fase 3 — Dati e funzionalità (settimane 2-6)
Il vantaggio competitivo possibile non è «più offerte dei generalisti» ma costo reale e chiarezza. Priorità:
1. Più negozi. Integrare zooplus (appena disponibile il feed), Arcaplanet, Amazon (solo tramite API ufficiale e nel rispetto dei termini sui prezzi), altri negozi specializzati italiani con feed o programmi affiliati. Ogni fonte con data di aggiornamento visibile.
2. Abbinamento prodotti per EAN/GTIN, con regole di normalizzazione di marca, linea, taglia, formato. Pagina prodotto unica con tutte le offerte confrontate. Gli abbinamenti incerti restano separati e segnalati.
3. Prezzo totale stimato (prodotto + spedizione secondo le soglie del negozio) come ordinamento di default, con spiegazione chiara.
4. Storico prezzi per prodotto (grafico semplice 30/90/180 giorni, minimo e massimo reali osservati dal sito). Salvare ogni rilevamento con data.
5. Avvisi di prezzo via email (double opt-in, cancellazione con un clic): «avvisami se scende sotto X €». Alimenta anche la newsletter settimanale, oggi «in preparazione».
6. Costo giornaliero integrato nella scheda prodotto: estrarre la razione dalle tabelle del produttore solo se verificabile; altrimenti campo manuale con peso e razione pre-compilabili dall'utente.
7. Lista «Il mio carrello risparmio» (salvata nel browser): permette di confrontare il costo di più prodotti per un negozio unico, tenendo conto delle spese di spedizione.
8. Segnalazione errori accanto a ogni prezzo («prezzo sbagliato?») collegata a un indirizzo o modulo, con tempi di risposta dichiarati.
4. Fase 4 — Contenuti e autorevolezza (continuo, dalla settimana 2)
Google premia utilità, esperienza e affidabilità. Il sito deve avere un'identità riconoscibile e contenuti che nessun generalista ha.
1. Pagine «Chi siamo» e «Metodo» solide: chi gestisce il sito, come vengono raccolti i dati, come si guadagna, come si correggono gli errori, contatti reali. Se possibile, un nome e un volto responsabili.
2. Pagine per marca e per linea (Royal Canin, Purina, Farmina, Monge, Trainer…): panoramica delle linee, formati, fasce di prezzo al kg osservate, offerte attuali. Testo originale e utile, non riempitivo. Una pagina nasce solo se ci sono dati sufficienti.
3. Guide basate su dati propri, ad esempio:
    ◦ «Quanto costa davvero nutrire un cane di taglia media ogni mese» (con calcolo dal catalogo);
    ◦ «Crocchette: prezzo al kg o costo giornaliero? Un confronto con esempi reali»;
    ◦ «Dove conviene comprare la lettiera per gatti: spedizione inclusa»;
    ◦ «Come leggere l'etichetta di un alimento per cani e gatti». Ogni guida: autore, data di aggiornamento, fonti citate (etichette, produttori, studi, test indipendenti), niente affermazioni sanitarie non verificate.
4. Osservatorio prezzi mensile (indice dei prezzi per categoria calcolato dai dati del sito). È il contenuto con più probabilità di ottenere citazioni spontanee da giornalisti, blog e community.
5. Parere veterinario: coinvolgere un veterinario o un nutrizionista per rivedere le guide e inserirne nome e qualifica (solo con accordo reale).
6. Aggiornamento: ogni guida ha data di revisione e viene riverificata ogni 3-6 mesi; le pagine non più valide vengono unite o rimosse con redirect 301.
7. Lingua e stile: italiano chiaro, frasi brevi, tono amichevole ma sobrio. Nessuna promessa assoluta («il migliore»), ma criteri espliciti.
5. Fase 5 — Grafica e UX (settimane 2-5)
Oggi l'identità è gradevole ma generica (teal, illustrazione SVG con cane e gatto, emoji). Obiettivo: aspetto da prodotto professionale, mantenendo calore e leggibilità.
1. Design system minimo: variabili CSS per colori, spaziature, raggi, ombre, tipografia. Palette di partenza dal teal #267c76 (già usato), con una tinta chiara, un accento caldo per le offerte (non rosso aggressivo) e un grigio neutro per i testi. Verificare i contrasti AA.
2. Tipografia: un solo carattere per i titoli e uno per il testo (o un'unica famiglia variabile), self-hosted, con font-display: swap, ben calibrata su mobile. Dimensione base 16-18 px, interlinea 1,5.
3. Home: sopra la piega solo tre cose: titolo chiaro con il valore («Confronta il prezzo reale di cibo e lettiere per cani e gatti»), barra di ricerca grande con suggerimenti automatici, ed esempi di risparmio reali. Sotto: categorie con icone coerenti, offerte reali, come funziona, fonti.
4. Eliminare i placeholder: mai «Caricamento…» senza scheletro; usare skeleton screen e un fallback testuale con i dati già presenti nell'HTML.
5. Scheda prodotto/offerta: immagine, nome, formato, prezzo, prezzo/kg, spedizione stimata, negozio con logo, data di rilevamento, pulsante chiaro «Vai al negozio». Etichette «Miglior prezzo totale» solo se calcolate sui dati reali.
6. Comparatore: tabella confrontabile con intestazioni fisse, evidenza visiva delle differenze, versione mobile a schede scorrevoli, stato vuoto utile, filtri sempre visibili e azzerabili.
7. Immagini: foto o illustrazioni originali e leggere (AVIF/WebP, srcset, loading="lazy", dimensioni dichiarate). Evitare immagini di stock generiche. Usare solo immagini di prodotto concesse dai feed o dai programmi affiliati.
8. Microinterazioni sobrie: transizioni brevi, rispetto di prefers-reduced-motion, modalità scura con prefers-color-scheme.
9. Pubblicità: pochi slot, mai sopra il contenuto principale né dentro la tabella del comparatore; etichetta «Pubblicità» chiara. Misurare l'effetto sulle metriche di coinvolgimento prima di aggiungerne altri.
10. Mobile first: pulsanti da almeno 44 px, ricerca sempre raggiungibile, menu semplice, nessuno scroll orizzontale.
6. Fase 6 — Fiducia, legalità, qualità percepita
• Banner cookie conforme, che non blocchi la lettura; categorie di cookie spiegate.
• Pagine Privacy, Cookie, Trasparenza e Pubblicità aggiornate e collegate dal footer.
• Indicare in ogni pagina con offerte: data dell'ultimo aggiornamento, fonte, avviso «prezzi non in tempo reale».
• Pagina «Correzioni»: registro pubblico degli errori segnalati e corretti.
• Controlli automatici sulla qualità dei dati: prezzi anomali (±50% rispetto alla mediana), peso/kg incoerente, offerte non più disponibili, link rotti. Le offerte sospette vengono nascoste automaticamente e registrate.
7. Fase 7 — Popolarità e acquisizione (dal mese 1)
L'IA può preparare materiali e analisi; i contatti e le pubblicazioni vanno approvati da una persona.
1. Digital PR basata sui dati: proporre a blog, testate locali, giornali di settore e community di proprietari di animali l'«Osservatorio prezzi» e le guide, con grafici scaricabili e metodo spiegato.
2. Directory e community pertinenti: segnalare il sito dove consentito (forum e gruppi di proprietari di cani e gatti, Reddit italiano, Telegram/Facebook di risparmio), rispettando le regole di ciascuna community e senza spam.
3. Collaborazioni: allevatori, toelettatori, veterinari, associazioni di adozione, blogger di settore. Offrire utilità (strumenti, dati), non scambi di link.
4. Newsletter: attivare il servizio email, con modulo semplice, benvenuto automatico e una email settimanale con 5-8 offerte verificate più un consiglio pratico. Segmentare per cane/gatto.
5. Social: riutilizzare i dati in formato breve (carosello «quanto costa al giorno…», confronto del mese), con una cadenza sostenibile.
6. Condivisione: pulsante «condividi il confronto» (già previsto) con anteprima sociale generata automaticamente.
7. Brand: valutare un nome e un logo più distintivi, e verificare che dominio, profili social e marchio siano coerenti.
8. Fase 8 — Misurazione e ciclo di miglioramento
KPI da monitorare ogni settimana, con valore iniziale registrato nell'audit:
Area
KPI
Indicizzazione
Pagine indicizzate in Search Console, errori di copertura
Visibilità
Impressioni, clic, CTR, posizione media per gruppo di query
Traffico
Sessioni organiche, utenti di ritorno, iscritti alla newsletter
Qualità
Core Web Vitals (CrUX/PageSpeed), punteggio accessibilità
Prodotto
Ricerche eseguite, confronti avviati, clic in uscita verso i negozi
Dati
Prodotti abbinati tra più negozi, età media dei prezzi, errori segnalati
Ricavi
Ricavo per sessione, click-through verso affiliati, impatto degli annunci sul coinvolgimento
Ogni due settimane l'IA produce un breve report: cosa è cambiato, cosa ha funzionato, cosa proporre come prossimo esperimento. Gli esperimenti (titoli, layout, ordinamento) si testano uno alla volta.
9. Piano 30 / 60 / 90 giorni
Giorni 1-30: fondamenta
• Audit completo, configurazione di Search Console e analytics.
• Pre-rendering delle pagine principali, sitemap, dati strutturati, canonical e pulizia degli URL.
• Correzione di performance e accessibilità.
• Nuovo design system e restyling di home, comparatore e scheda prodotto.
• Integrazione di almeno un nuovo negozio importante.
Giorni 31-60: valore e contenuti
• Pagine prodotto abbinate per EAN, storico prezzi, prezzo totale con spedizione.
• Pagine marca e prime 6-8 guide originali con fonti e revisione.
• Newsletter attiva e avvisi di prezzo.
• Primo Osservatorio prezzi e prime azioni di PR.
Giorni 61-90: crescita
• Estensione di negozi e categorie (lettiere, snack, igiene, antiparassitari solo con controlli adeguati).
• Esperimenti su layout, ordinamento e posizionamento degli annunci.
• Rafforzamento di autorevolezza: parere veterinario, pagina Metodo con dati aggiornati, collaborazioni.
• Revisione dei risultati e piano per i successivi 90 giorni.
10. Come l'IA deve lavorare (istruzioni operative)
1. Iniziare dalla Fase 1 e non passare avanti senza aver presentato l'audit.
2. Per ogni fase: elencare i compiti, i file toccati, i rischi e come verificare il risultato (test, Lighthouse, validazione schema, controllo manuale).
3. Fare modifiche incrementali, con commit separati e messaggi descrittivi; non cambiare più aree critiche nello stesso commit.
4. Dove serve una decisione umana (budget, contatti esterni, accordi con negozi o veterinari, testi legali, scelta del marchio) fermarsi e chiedere, proponendo opzioni con pro e contro.
5. Dichiarare sempre cosa non si può verificare (posizioni in classifica future, effetti dei backlink, dati non accessibili) invece di promettere risultati.
6. A fine di ogni fase consegnare: riepilogo di cosa è stato fatto, metriche prima/dopo, elementi rimandati e prossimi passi consigliati.
Nota finale
Il percorso più credibile è diventare il sito più chiaro e affidabile sul costo reale del mantenere un cane o un gatto, non un clone dei comparatori generalisti. Trasparenza già presente, dati aggiornati, strumenti utili e contenuti originali sono la base su cui costruire popolarità e posizionamento in modo duraturo.