# Newsletter — attivazione del 25 ottobre 2026

## Evidenze
- Titolare e recapito già pubblicati: Mirco Drighetto, capobranco@offerte4zampe.it. Nessun nuovo dato personale ricavato dalla memoria.
- Prova reale autorizzata: DOI ricevuta in Gmail INBOX dal mittente corretto, SPF/DKIM/DMARC pass; iscrizione confermata alla lista #3; revoca dal modulo pubblico e Campagne email Bloccato osservato per il solo indirizzo di prova. Nessun invio massivo.
- Informativa newsletter aggiornata: finalità promozionali, consenso facoltativo, dati tecnici, Brevo responsabile/DPA appendice3, trasferimenti, criteri di conservazione, revoca e diritti. Non promette cancellazione automatica non configurata.
- Brevo: consenso al pixel tracking per contatto attivato; monitoraggio del consenso sconosciuto No. Salvato e riletto dopo reload. Nessuna casella di consenso al tracking nel modulo: i nuovi iscritti restano sconosciuti e non monitorati individualmente.
- Marketing/Campagne accessibile, bozza #5 modificabile, mittente capobranco corretto, nessun avviso di sospensione osservato. AUP corrente controllata: newsletter editoriale pet a opt-in, nessuna lista acquistata/scraped o vendita di lead.
- Ambito dei permessi: email con link alle pagine editoriali del proprio sito. NON autorizza directlink affiliati, immagini feed o DEM merchant: servono condizioni specifiche del singolo programma prima di introdurli nelle email.
- Bozza #5 aggiornata senza prezzi del19ottobre ormai obsoleti: consigli confronto e Preferiti, soli link al sito, footer identità/privacy e segnaposto Brevo {{ unsubscribe }}. Oggetto e anteprima coerenti. Nessun destinatario selezionato e nessun invio/schedulazione.
- Homepage e pagina newsletter allineate alle iscrizioni; modulo esterno caricato solo su scelta dell’utente. Le cinque verifiche restano obbligatorie nel frontend; errore rete o gate mancante non espone iscrizioni.

## Conservazione operativa
L’invio usa soltanto iscrizioni confermate alla lista newsletter. Revoca: soppressione immediata per campagne; non riattivare contatti manualmente. Richieste accesso/cancellazione arrivano a capobranco e si gestiscono in Brevo. Verificare periodicamente richieste non confermate e dati residui: rimuovere ciò che non è più necessario; mantenere soltanto prova consenso/revoca e soppressione necessarie a rispettare le scelte, senza riuso promozionale. Nessuna esportazione iscritti nel repository.

## Fonti consultate il 25 ottobre
- https://www.brevo.com/legal/antispampolicy/ — AUP, consenso esplicito e prova, no liste comprate/scraped, unsubscribe marketing obbligatorio.
- https://www.brevo.com/legal/termsofuse/ — DPA appendice3 già parte delle condizioni del servizio; titolare/responsabile, retention a carico cliente e trasferimenti.
- https://help.brevo.com/hc/it/articles/37113920427922 — configurazione consenso pixel per contatto e stato sconosciuto No.
- https://help.brevo.com/hc/en-us/articles/209553645-Insert-a-custom-unsubscribe-link-in-your-emails — segnaposto HTML unsubscribe.
- https://www.garanteprivacy.it/home/i-miei-diritti/diritti — diritti interessato.

Test locali superati: 95 Python e78 Node. CI mobile e deploy da registrare dopo pubblicazione. Raccolta newsletter distinta da invio automatico e dagli alert prezzo, tuttora non attivi.

### Verifica conclusa
Commit funzionale94932081ad8e92f8ba496a1accae555303740c40 e aggiornamento CI f8412a5a9cdeff2881371ad316df20994b846909: Cloudflare Workers Build e mobile success. CI finale40184636049 include95 Python e78 Node, modulo visibile/cancellazione e prove mobile. Pagina pubblica https://offerte4zampe.it/newsletter osservata con iscrizioni aperte, link effettivo al modulo Brevo con checkbox non preselezionata, /privacy#newsletter con testo aggiornato e CTA pubblica di disiscrizione. Nessuna nuova email di prova, campagna, schedulazione o revisione AdSense inviata in questa attivazione. Prima email aggiornata resta bozza#5 senza destinatari.
