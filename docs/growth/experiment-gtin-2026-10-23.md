# Esperimento acquisizione GTIN — 23 ottobre 2026 (proposta, NON pubblicata)

## Scopo e motivazione
Trasformare il [kit editoriale del 21 ottobre](acquisition-kit-2026-10-21.md) in un solo test di acquisizione organica, senza duplicare le tre bozze già pronte. La destinazione è la guida esistente **[Stesso prodotto o solo un nome simile?](https://offerte4zampe.it/stesso-prodotto-formato-gtin)**, non una nuova pagina SEO concorrente. L'ultima verifica documentata di Search Console (17–20 ottobre) mostra 2 clic e 9 impressioni e una query non relativa ai prodotti per animali; **la scelta è un'ipotesi, non una pagina con impressioni pet verificate**.

## Landing e confronto reale
- Il generatore `automation/build_savings_guides.py` seleziona fino a due gruppi recenti con GTIN valido, stessa marca e peso netto. La guida espone i prezzi, il negozio e la data per ogni riga, senza dichiarare equivalenza nutrizionale.
- Esempio documentato nell'HTML repository del **23 ottobre 2026, ore 06:49 UTC**: Almo Nature Holistic Anti Hairball con manzo, bustina 70 g, GTIN **08001154125887**; Animaliapet **1,15 €**, Isola dei Tesori **1,29 €**. Differenza tra prezzi di confezione **0,14 €**, spedizione esclusa. [Confronto interno](https://offerte4zampe.it/prezzi-08001154125887-afffacdfaa). Dati storici di rilevazione, **non prezzi correnti garantiti**.
- **Controllo qualità da risolvere prima di promuovere l'altro esempio:** per il GTIN `08001154000221` (Almo Nature Daily 12 kg) il titolo importato da Bauzaar indica «Daily», ma il percorso dell'URL destinazione contiene «holistic-mantenimento». Potrebbe essere uno slug storico, non una prova di errore; verificare manualmente la variante reale prima di citarlo come confronto affidabile. Non aprire link affiliati per testare l'attribuzione.
- Il generatore ora prevede una CTA per ciascun gruppo verso la pagina statica di confronto GTIN (es. `/prezzi-08001154000221-4e250c0f7d` vista nell'indice del repository), mantenendo i collegamenti alle schede interne e il metodo indipendente dalle commissioni. La generazione pubblica e il deploy restano da verificare.
- Percorso previsto: guida → confronto statico dello stesso formato → scheda/offerte → scelta esplicita del negozio. Non cliccare link affiliati per testarlo.
- Link interni già presenti: `/guide-risparmio`, `/prezzo-confezione-o-prezzo-kg`, `/spedizione-gratuita-conviene`, `/confronta-cibo`, `/carrello-risparmio`. Nessun nuovo testo duplicato aggiunto alla homepage.

## Canale Reddit scartato dopo verifica delle regole (23 ottobre 2026, 16:18 Europe/Rome)
La sidebar pubblica di [r/ItaliaPersonalFinance](https://www.reddit.com/r/ItaliaPersonalFinance/) dichiara: «È vietato sponsorizzare le proprie attività e/o sponsorizzare fonti di guadagno in cui si è direttamente coinvolti». Testo osservabile anche nella [pagina Reddit in italiano](https://it.reddit.com/r/ItaliaPersonalFinance/comments/vhkkgz/gli_stipendi_da_1200_euro_in_italia/). La bozza Reddit preparata in precedenza è **ritirata, non autorizzabile per questo subreddit**; non pubblicare, non riproporre sotto altro account e non aggirare la regola. La pagina /about/rules non era accessibile dal browser di ricerca, ma il divieto compare nella descrizione pubblica del subreddit.

## Unico canale sostitutivo proposto: Instagram, profilo del progetto @offerte4zampe
**Destinatari:** persone che già seguono il profilo e hanno interesse per la spesa per cani e gatti; pubblico, reach e accesso all'account **non verificati** in questa esecuzione. Il titolare ha dichiarato di possedere il profilo, non serve crearne uno nuovo. Nessun invio a terzi e nessuna pubblicazione.

**Formato:** una sola storia organica con testo su sfondo neutro creato nell'editor Instagram, senza immagini di prodotti né loghi di negozi. È un adattamento mirato del contenuto GTIN già presente nel kit, non un nuovo articolo SEO. Se l'account non dispone dello sticker Link, non pubblicare con un collegamento inesistente. Verificare nell'app la disponibilità della funzione e le [Linee guida della community Instagram](https://help.instagram.com/477434105621119); evitare tag di utenti, DM automatici, repost ripetuti e sponsorizzazioni a pagamento. Il [Centro trasparenza Meta](https://transparency.meta.com/policies/community-standards/spam/) illustra i limiti anti-spam della piattaforma.

### Unico contenuto da approvare: storia Instagram
**Testo visibile (una schermata):**

> Stesso nome, stesso prodotto? 🐾
>
> Prima di confrontare i prezzi controlla **codice GTIN, formato e quantità**. Due confezioni simili non sono sempre uguali.
>
> Nella nostra guida gratuita trovi esempi datati da più negozi e il confronto dello stesso formato.
>
> **Prezzi rilevati, non in tempo reale. Affiliazioni dichiarate.**

**Sticker link:** «Apri la guida» → https://offerte4zampe.it/stesso-prodotto-formato-gtin

**Descrizione accessibile:** «Guida gratuita per verificare GTIN, peso netto e formato prima di confrontare prezzi di prodotti per animali. I dati sono rilevazioni datate; possibili link affiliati dichiarati.» Non citare prezzi singoli nella storia, perché possono cambiare prima della pubblicazione. Se lo sticker non è disponibile, il testo non deve suggerire un link cliccabile.

### Gate prima della pubblicazione
1. Approvazione specifica del titolare per **questa singola storia** su **@offerte4zampe**; non dedurre consenso dall'autorizzazione a modificare GitHub.
2. Verifica dal profilo autorizzato delle regole, dell'effettiva disponibilità dello sticker Link, del testo e della destinazione. Nessun accesso Instagram o Metricool è stato eseguito qui.
3. Conferma HTTP/browser della guida e del confronto interno, rilevazioni datate e disclosure/privacy; i tentativi di apertura web del 23 ottobre non sono riusciti per errore dello strumento e **non dimostrano downtime**.
4. Nessun tracking aggiuntivo senza requisiti privacy/consenso verificati; nessun click affiliato, test pubblicitario o pubblicazione autonoma.

## Misurazione senza inventare risultati
- **Baseline:** finestra 16–22 ottobre 2026, Search Console clic/impressioni organiche per la URL landing e query; Analytics, se autorizzati, sessioni con referrer Instagram e Insights della storia (visualizzazioni e tocchi sticker, se accessibili). Valori attuali **non disponibili**. I 2 clic/9 impressioni storici riguardano l'intero sito nel 17–20 ottobre e non sono baseline della pagina.
- **Osservazione:** 24 ore per le metriche della storia e sette giorni dalla pubblicazione effettiva (T+0…T+7) per i dati del sito, con controllo a T+3 e T+7 e ritardo fisiologico Search Console. Se non si pubblica, **nessuna finestra post** e nessuna attribuzione.
- **Funnel distinto:** impressioni/clic organici Search Console ≠ sessioni analytics ≠ clic affiliati network ≠ ordini ≠ commissioni (pendenti/approvate/pagate). Registrare per ogni fonte intervallo, timezone e data lettura. Non attribuire a Instagram i clic network senza referrer/campagna verificati. Escludere test/bot solo quando identificabili; non creare traffico di prova.
- **Criterio di decisione:** valutare se aumentano sessioni qualificate e apertura dei confronti, senza promessa di significatività con piccoli campioni; la prima monetizzazione richiede una commissione effettiva verificata in network/AdSense, con data, importo e stato.

**Stato:** pacchetto predisposto nel repository; nessuna pubblicazione esterna, invio, spesa, iscrizione o campagna effettuata.
