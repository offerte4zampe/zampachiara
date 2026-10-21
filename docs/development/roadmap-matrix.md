# Matrice di completamento roadmap

Aggiornata il 21 ottobre 2026. Questa matrice distingue implementazione verificata, lavoro predisposto ma non attivo e dipendenze esterne. Non attribuisce risultati SEO, vendite o conformità legale senza evidenze.

| Area | Stato | Evidenza attuale | Residuo o dipendenza |
|---|---|---|---|
| Audit iniziale | Completato | Audit repository, Lighthouse mobile precedente, inventario contenuti/catalogo e report in `docs/development` | Le metriche sul campo richiedono traffico CrUX sufficiente |
| Rendering e SEO tecnica | Completato per le pagine attuali | HTML prerenderizzato, canonical, sitemap divise, pagine marca/categoria/prodotto, breadcrumb e dati strutturati supportati | Invio/controllo indicizzazione in Search Console è attività esterna; nessuna posizione garantita |
| Qualità HTML automatica | Completato | `automation/audit_site.py`, report `/data/site-quality.json`, pipeline bloccante | Non sostituisce revisione manuale WCAG o validazione legale |
| Catalogo e aggiornamento | Completato per quattro fonti correnti | Import ogni 6 ore, freschezza, fallback snapshot, quarantena anomalie e controllo progressivo link | Nuovi negozi richiedono approvazioni/feed/API |
| Abbinamento prodotti | Completato in modo conservativo | GTIN valido + marca + peso netto; formati incerti separati | Multipack Isola esclusi finché la base quantità non è verificata |
| Prezzo totale e spedizione | Completato dove le regole sono note | Carrello, quantità, stessa lista e soglie con fonte/data; nessun vincitore su dati incompleti | Località, servizi e soglie ambigue restano non disponibili |
| Storico prezzi | Completato | Osservazioni giornaliere, identità, finestre 30/90/180, shard lazy | La profondità cresce solo col tempo; nessun backfill |
| Costo giornaliero | Completato con input manuale | Calcolo confezione/kg/giorno/30 giorni senza razione inventata | Tabelle produttore non importate senza fonte verificata |
| Ricerca e UX mobile | Completato | Suggerimenti accessibili, tastiera/tocco, stati vuoti, test 393×852, nessun overflow nei test | Modalità scura secondo dispositivo implementata con prova colori/overflow su sei pagine; restano verifiche manuali complete WCAG e device reali |
| Condivisione prodotto | Implementata e osservata sul dominio | Link interno con ID esatto, copia/fallback, OG testuali generati dal Worker con shard titolo; confronto e noindex conservati | Immagine generica del progetto, cache delle anteprime esterne non controllabile |
| Pagine per linea | Prima linea completata e pubblica | Monge BWild, fonte ufficiale,26 offerte/tre negozi nel ciclo21 ottobre,24 schede; titoli interni, breadcrumb e sitemap | Estensione editoriale ad altre linee solo con tassonomia verificata e dati sufficienti; nessuna equivalenza nutrizionale |
| Segnalazioni e correzioni | Completato | Bozza locale mailto, allowlist, registro pubblico, controlli automatici | La presa in carico umana delle segnalazioni non è automatizzabile senza leggere/inviare posta |
| Guide originali | Obiettivo minimo completato | Sei guide generate da dati correnti, testate e collegate | Altre due guide sono facoltative entro l’obiettivo 6–8; revisione veterinaria richiede accordo reale |
| Osservatorio prezzi | Infrastruttura completata | Pagina, JSON, metodo e copertura; 145 righe categoria/mese al primo ciclo | Zero indici pubblicabili finché non esistono due mesi chiusi con pannello minimo |
| Affiliazioni | Parzialmente attive | Bauzaar e Isola tracciati con disclosure e `rel=sponsored`; ordine indipendente dalle commissioni | Amazon: sette schede/quattro ASIN con link editoriali diretti verificati, senza prezzo/stock; prezzi automatici richiedono API ufficiali. Altri merchant richiedono approvazione/feed |
| Pubblicità | Predisposta, non pienamente verificata | Metadati/ads.txt e spazi predisposti; loader AdSense rimosso finché CMP/account non verificati | Stato account, CMP e ricavi richiedono accesso/consenso verificato |
| Newsletter Brevo | Predisposta, non attiva sul sito | Mittente/dominio, modulo con consenso separato e DOI provato; conferma iniziale finita nello spam | Cancellazione/soppressione, informativa e permessi contenuti ancora da verificare; nessuna campagna inviata |
| Avvisi prezzo | Infrastruttura offline | Schema e motore puro per soglia/consenso/replay | D1, callback autenticati, revoca, coda e invio richiedono configurazione remota e prove autorizzate |
| Privacy/cookie | Parziale | Titolare autorizzato, contatto, pagine informative e blocco funzionalità non pronte | Conservazione, ruoli/DPA, cancellazione e CMP effettiva richiedono decisioni/verifiche esterne |
| Analytics e KPI | Parziale | Metriche first-party minimizzate e audit tecnici | Search Console, traffico, ritorni e ricavi non sono disponibili dal repository |
| Acquisizione/PR | Materiali preparati, nessuna diffusione | `docs/growth/acquisition-kit-2026-10-21.md`: presentazione, proposta editoriale, tre post e testo carosello; fonti e controlli di rilascio | Pubblicazioni, contatti, community, social e collaborazioni richiedono approvazione umana; nessun indice o grafico di trend senza dati maturati |
| Parere veterinario | Bloccato esternamente | Nessuna qualifica dichiarata senza accordo | Serve professionista reale e consenso alla pubblicazione |
| Pubblicazione | Verificata per l’ultimo ciclo dati | GitHub Actions, Workers Build e report qualità letto sul dominio | Ogni modifica successiva va riverificata; una build riuscita non prova da sola il rendering pubblico |

## Criteri per dichiarare conclusa l’automazione

L’automazione può essere chiusa solo quando non rimane lavoro tecnico autorizzato e ripetibile senza nuove decisioni. La maturazione dello storico, gli accessi di terzi, le campagne, i contatti, i dati legali mancanti e gli accordi professionali sono dipendenze, non attività da simulare. In presenza di tali blocchi il progetto può essere tecnicamente operativo, ma non va descritto come completamente finito.

## Esito conclusivo tecnico, 21 ottobre 2026
Lavori autorizzati attualmente realizzabili conclusi e verificati. Ultimo browser CI: 57 Node,85 Python,312 pagine/zero problemi; Worker e fallback verificati. Audit cinque pagine: performance99–100, accessibilità/SEO/best practices100, comparatore TBT89,9 ms eLCP1954 ms in laboratorio. Pubblicazione funzionale osservata sul dominio. Restano tutte le dipendenze esterne elencate sopra: il progetto complessivo non è interamente finito. Il ciclo autonomo viene fermato per evitare ripetizioni; nuove integrazioni/attivazioni riprendono con dati o accessi verificabili.
