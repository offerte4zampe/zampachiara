# Matrice di completamento roadmap

Aggiornata il 20 ottobre 2026. Questa matrice distingue implementazione verificata, lavoro predisposto ma non attivo e dipendenze esterne. Non attribuisce risultati SEO, vendite o conformità legale senza evidenze.

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
| Ricerca e UX mobile | Completato | Suggerimenti accessibili, tastiera/tocco, stati vuoti, test 393×852, nessun overflow nei test | Modalità scura non prioritaria e non implementata |
| Segnalazioni e correzioni | Completato | Bozza locale mailto, allowlist, registro pubblico, controlli automatici | La presa in carico umana delle segnalazioni non è automatizzabile senza leggere/inviare posta |
| Guide originali | Obiettivo minimo completato | Sei guide generate da dati correnti, testate e collegate | Altre due guide sono facoltative entro l’obiettivo 6–8; revisione veterinaria richiede accordo reale |
| Osservatorio prezzi | Infrastruttura completata | Pagina, JSON, metodo e copertura; 145 righe categoria/mese al primo ciclo | Zero indici pubblicabili finché non esistono due mesi chiusi con pannello minimo |
| Affiliazioni | Parzialmente attive | Bauzaar e Isola tracciati con disclosure e `rel=sponsored`; ordine indipendente dalle commissioni | Amazon richiede accesso API/condizioni di qualificazione; altri merchant richiedono approvazione/feed |
| Pubblicità | Predisposta, non pienamente verificata | AdSense inserito e slot separati dal contenuto | Stato account, CMP e ricavi richiedono accesso/consenso verificato |
| Newsletter Brevo | Predisposta, non attiva sul sito | Mittente/dominio, modulo con consenso separato e DOI provato; conferma iniziale finita nello spam | Cancellazione/soppressione, informativa e permessi contenuti ancora da verificare; nessuna campagna inviata |
| Avvisi prezzo | Infrastruttura offline | Schema e motore puro per soglia/consenso/replay | D1, callback autenticati, revoca, coda e invio richiedono configurazione remota e prove autorizzate |
| Privacy/cookie | Parziale | Titolare autorizzato, contatto, pagine informative e blocco funzionalità non pronte | Conservazione, ruoli/DPA, cancellazione e CMP effettiva richiedono decisioni/verifiche esterne |
| Analytics e KPI | Parziale | Metriche first-party minimizzate e audit tecnici | Search Console, traffico, ritorni e ricavi non sono disponibili dal repository |
| Acquisizione/PR | Non eseguita | Osservatorio e dati scaricabili preparano una base reale | Pubblicazioni, contatti, community, social e collaborazioni richiedono approvazione umana |
| Parere veterinario | Bloccato esternamente | Nessuna qualifica dichiarata senza accordo | Serve professionista reale e consenso alla pubblicazione |
| Pubblicazione | Verificata per l’ultimo ciclo dati | GitHub Actions, Workers Build e report qualità letto sul dominio | Ogni modifica successiva va riverificata; una build riuscita non prova da sola il rendering pubblico |

## Criteri per dichiarare conclusa l’automazione

L’automazione può essere chiusa solo quando non rimane lavoro tecnico autorizzato e ripetibile senza nuove decisioni. La maturazione dello storico, gli accessi di terzi, le campagne, i contatti, i dati legali mancanti e gli accordi professionali sono dipendenze, non attività da simulare. In presenza di tali blocchi il progetto può essere tecnicamente operativo, ma non va descritto come completamente finito.
