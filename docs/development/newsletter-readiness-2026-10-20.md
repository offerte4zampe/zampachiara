# Attivazione newsletter: verifiche concrete

Verificato il 20 ottobre 2026 nel pannello Brevo e nel modulo pubblico, senza leggere contatti/iscritti o inviare email.

## Completato

- Mittente `Offerte a 4 Zampe <capobranco@offerte4zampe.it>` verificato. Dominio `offerte4zampe.it` autenticato nel pannello Domini, DMARC configurato.
- Modulo standard esistente «Offerte da fiutare», con consenso newsletter/promozioni distinto, checkbox obbligatoria e non selezionata nel modulo pubblico. Nessun consenso implicito agli alert individuali.
- Conferma configurata: **Email di conferma doppia**. Modello predefinito DOI #1 attivo; contiene il collegamento `{{ doubleoptin }}`.
- Corretto il mittente effettivo del modello DOI #1, che era ancora Gmail: selezionato capobranco e salvato, conferma UI «Modello salvato con successo». Nessuna prova o campagna inviata.
- Recuperato URL HTTPS ufficiale sibforms e inserito in `site/data/newsletter.json`; il frontend continua a richiedere tutti i requisiti. Non rendere visibile il modulo finché gli altri flag restano false.
- Testo pubblico del consenso e frequenza settimanale verificati. Nessun codice esclusivo o sconto garantito promesso.

## Da completare prima di aprire il modulo sul sito

1. **Informativa effettiva**: l'attuale `/privacy#newsletter` dice ancora che il servizio è in preparazione e che identità/recapiti del titolare e conservazione sono da completare. Occorrono i dati che il titolare intende pubblicare e la politica di conservazione effettiva; non usare dati personali tratti dalla memoria. Una denominazione di progetto non identifica automaticamente il titolare.
2. **Prova di invio autorizzata** a un indirizzo controllato dal titolare: verificare recapito della DOI da capobranco, conferma e cancellazione/soppressione. Il ritorno alla pagina di ringraziamento non prova la conferma. Non leggere la lista degli iscritti; usare soltanto l'indirizzo di prova e un riscontro del titolare o un controllo puntuale autorizzato.
3. **Cancellazione**: Brevo documenta un link/pagina predefiniti nelle campagne. Questo non dimostra che il futuro modello settimanale sia corretto; va verificato sul modello effettivo e in una prova autorizzata. Il modello #4 di conferma disiscrizione esiste, ma non è stato usato né inviato.
4. **Permessi di invio e contenuti**: confermare che il canale previsto sia utilizzabile e verificare eventuali approvazioni dei merchant prima di inserire link/creatività affiliati nelle email. La sola approvazione della campagna per il sito non autorizza automaticamente DEM. Non inviare campagne, creare automazioni o fingere approvazioni mancanti.

`double_opt_in_verified`, `unsubscribe_verified`, `privacy_notice_verified`, `provider_permissions_verified` restano false: configurazione osservata e funzionamento provato sono due evidenze diverse. `separate_consent_verified` è true perché requisito obbligatorio e stato non selezionato sono stati letti nel modulo pubblico.

## Cosa il sito mostra ancora come in preparazione

La ricerca nei file pubblici ha individuato questa dicitura per la newsletter (home, pagina newsletter e informativa). Comparatore, carrello, costo giornaliero e storico sono già utilizzabili. Gli alert via email sono predisposti offline, senza endpoint, database remoto o invio. Amazon/API, analytics autenticata e nuovi feed richiedono gli accessi già registrati in STATUS; non sostituirli con segnaposto.

## Fonti operative

- https://help.brevo.com/hc/en-us/articles/208771869-Create-a-sign-up-form-in-Brevo
- https://help.brevo.com/hc/en-us/articles/360019540880-Create-a-custom-double-opt-in-DOI-email-template-for-a-sign-up-form-created-in-Brevo
- https://help.brevo.com/hc/en-us/articles/209553645-Insert-a-custom-unsubscribe-link-in-your-emails

Per l'indirizzo ospitato usare esclusivamente `site/data/newsletter.json`, senza duplicarlo in HTML o aggiungere chiavi API. Si tratta di un URL pubblico di modulo, non di una credenziale.
