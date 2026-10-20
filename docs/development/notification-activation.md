# Newsletter e avvisi: infrastruttura preparata, servizio disattivato

Stato al 20 ottobre 2026: nessuna raccolta email nuova, nessun invio, database remoto, endpoint di iscrizione o pianificazione di notifiche. Il mittente previsto è capobranco@offerte4zampe.it. Non sono stati letti account o liste iscritti per questa implementazione.

## Componenti disponibili

- `site/assets/newsletter-readiness.js` convalida il modulo HTTPS Brevo e tutti i flag, non soltanto DOI e cancellazione. `newsletter.json` mantiene URL nullo e tutti i flag false.
- `worker/notification-plan.mjs` è un modulo puro non collegato al Worker: produce una decisione, non una email. Richiede conferma e versione informativa per la finalità price_alert, identità esatta dell'offerta, disponibilità e data recente. Newsletter non implica consenso agli avvisi. La soglia è il prezzo della confezione in centesimi, spedizione esclusa.
- Primo rilevamento, intervalli oltre 36 ore, prezzi già sotto soglia, replay e cambi di prodotto non producono un avviso. Serve un passaggio osservato da prezzo pari/sopra soglia a prezzo strettamente inferiore. Una nuova osservazione deve essere successiva alla conferma; nessun recupero retroattivo di notifiche.
- `worker/schema/0001_notifications.sql` è una migrazione predisposta e testata solo su SQLite in memoria. Distingue i consensi per finalità e impedisce conferme mancanti e duplicati nella coda. Nessun binding D1 è stato configurato e nessuna migrazione remota applicata. Non contiene email, IP o corpi dei messaggi; il riferimento al contatto del fornitore resta comunque un dato da gestire nell'informativa e nella conservazione.

## Dipendenze per l'attivazione

Restano da verificare identità e informativa del titolare, tempi di conservazione/cancellazione, consensi separati, permessi del programma affiliato per i contenuti email e autorizzazione del fornitore. Non sostituire queste informazioni con segnaposto. Conservare ogni evidenza nel registro di progetto prima di cambiare i flag.

Prima di implementare la raccolta occorrono gli ID reali della lista e del template DOI, URL di conferma, accesso alle credenziali come secret del server e verifica della cancellazione/soppressione presso il fornitore. Non inserire chiavi API nel repository o negli asset pubblici. Il modulo pubblico resta nascosto finché manca un requisito.

## Integrazione successiva, solo con requisiti verificati

1. Finalizzare privacy, modalità di consenso, conservazione e procedure di cancellazione; verificare permessi dei negozi. Registrare gli esiti reali, senza auto-attestazioni.
2. Configurare il modulo ospitato e template Brevo effettivi. L'endpoint DOI documentato `POST /v3/contacts/doubleOptinConfirmation` invia una email di conferma: non è stato chiamato e richiede autorizzazione all'invio prima di una prova con indirizzo controllato dal titolare. Un ritorno alla pagina di ringraziamento non basta come prova dell'attivazione del contatto.
3. Implementare e testare l'adattatore server, autenticazione dei callback e verifica del consenso effettivo senza fidarsi di dati dal browser. Inserire i contatti soltanto nella finalità scelta; non esportare gli iscritti in GitHub o nel sito.
4. Solo dopo la decisione sul database, configurare un binding e applicare la migrazione in ambiente di prova. Verificare schema e cancellazione prima della produzione. Pianificatore e invio sono ancora da implementare e autorizzare.
5. Il valutatore deve aggiornare stato e coda in una transazione con chiave univoca. Il mittente deve ricontrollare il consenso immediatamente prima di ogni invio, scartare eventi superati, applicare soppressioni e gestire esiti incerti senza duplicare messaggi. La sola decisione `notify` non autorizza l'invio.
6. Implementare cancellazione con un clic e token non esposti nei log, revoca per finalità e gestione della coda pendente. Definire limiti di frequenza, anti-abuso e conservazione; manca ancora questo adattatore.
7. Eseguire prove autorizzate di DOI, revoca, cancellazione e recapito con contatti di prova del titolare, documentarne gli esiti, quindi modificare i flag e aprire il modulo. Non spedire campagne durante lo sviluppo autonomo richiesto.

## Fonti primarie consultate

- Brevo, Create Contact via DOI: https://developers.brevo.com/reference/create-doi-contact . Documenta email, lista, template e redirect richiesti; non è stata inviata alcuna richiesta autenticata.
- Cloudflare D1, migrations: https://developers.cloudflare.com/d1/reference/migrations/ . Preparare un file SQL non crea un database né applica una migrazione remota.

Questa predisposizione non certifica conformità legale, consegna email o configurazione dell'account.
