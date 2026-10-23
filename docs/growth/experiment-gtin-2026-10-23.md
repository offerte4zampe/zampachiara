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

## Un solo canale candidato: Reddit r/ItaliaPersonalFinance
**Destinatari pubblici pertinenti:** utenti della community interessati al budget per animali, non individui da contattare. La pertinenza è supportata da una discussione pubblica sul costo di due gatti (17 marzo 2026): https://www.reddit.com/r/ItaliaPersonalFinance/comments/1rw8ocf/mantenere_bene_un_animale_domestico_costa/ . Non intervenire automaticamente nel vecchio thread e non inviare DM.

**Regole ufficiali:** Reddit vieta spam, ripetizione e promozione non richiesta: https://support.reddithelp.com/hc/it/articles/360043504051-Spam . La documentazione moderatori precisa che la promozione non è sempre vietata, ma le singole community possono vietarla o limitarla: https://support.reddithelp.com/hc/en-us/articles/28012014962580-How-do-I-keep-spam-out-of-my-community . Prima di proporre una pubblicazione effettiva leggere le regole correnti del subreddit: https://www.reddit.com/r/ItaliaPersonalFinance/about/rules . **Le regole specifiche non sono state verificate in questa esecuzione; nessuna autorizzazione a pubblicare può essere presunta.** Se vietano autopromozione/link, non pubblicare e non aggirare il divieto.

### Unico testo proposto per approvazione
**Titolo:** Confrontare le crocchette: perché il nome non basta (GTIN e formato)

> Quando si prova a risparmiare sul cibo per animali, confrontare due sacchi con un nome simile può portare fuori strada: cambia la ricetta, il peso o il multipack. Per confrontare *lo stesso* articolo conviene controllare GTIN, marca e quantità netta, poi aggiungere la spedizione al totale. Ho lavorato a una guida gratuita con esempi datati di offerte realmente rilevate da più negozi: https://offerte4zampe.it/stesso-prodotto-formato-gtin . Sono coinvolto nel progetto Offerte a 4 Zampe: alcuni link ai negozi sono affiliati e dichiarati, ma non cambiano l'ordinamento. Prezzi e disponibilità vanno ricontrollati prima di acquistare. Come controllate che due confezioni siano davvero identiche?

Testo educativo, una sola pubblicazione eventuale; non ripetere il post in più community, non fare crosspost automatizzati. Nessun link di tracking nuovo né invito a cliccare pubblicità.

## Gate prima della pubblicazione
1. Autorizzazione **specifica** del titolare per questo testo e questa community, non dedotta dall'autorizzazione a sviluppare il repository.
2. Verifica delle regole della community e compatibilità con autopromozione/disclosure; se vietata, scartare il canale senza eludere il filtro.
3. Conferma HTTP/browser che la landing e almeno un confronto interno si aprano, che le offerte mostrate siano fresche e che la disclosure/privacy siano complete; non testare uscite affiliate.
4. Controllo dati del catalogo al momento del post; se gli esempi sono cambiati, il post resta valido senza numeri puntuali, ma la landing deve riportare rilevazioni verificabili.

## Misurazione senza inventare risultati
- **Baseline:** finestra 16–22 ottobre 2026, Search Console clic/impressioni organiche per la URL landing e query; Analytics, se autorizzati, sessioni con referrer Reddit. Valori attuali **non disponibili**. I 2 clic/9 impressioni storici riguardano l'intero sito nel 17–20 ottobre e non sono baseline della pagina.
- **Osservazione:** sette giorni dalla data di pubblicazione effettiva (T+0…T+7), con controllo a T+3 e T+7 e ritardo fisiologico Search Console. Se non si pubblica, **nessuna finestra post** e nessuna attribuzione.
- **Funnel distinto:** impressioni/clic organici Search Console ≠ sessioni analytics ≠ clic affiliati network ≠ ordini ≠ commissioni (pendenti/approvate/pagate). Registrare per ogni fonte intervallo, timezone e data lettura. Non attribuire a Reddit i clic network senza referrer/campagna verificati. Escludere test/bot solo quando identificabili; non creare traffico di prova.
- **Criterio di decisione:** valutare se aumentano sessioni qualificate e apertura dei confronti, senza promessa di significatività con piccoli campioni; la prima monetizzazione richiede una commissione effettiva verificata in network/AdSense, con data, importo e stato.

**Stato:** pacchetto predisposto nel repository; nessuna pubblicazione esterna, invio, spesa, iscrizione o campagna effettuata.
