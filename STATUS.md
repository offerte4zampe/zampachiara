# Stato operativo — Offerte a 4 Zampe

Ultima verifica: 2026-10-23 (Europe/Rome). Repository `offerte4zampe/zampachiara`, branch `main`. Questo registro distingue osservazioni sul codice, verifiche dei pannelli e dati commerciali; non è una prova di deploy o di ricavo.

## Evidenze di questa verifica
- HEAD letto prima della scrittura: `a5313f387d0bd6ed9f513938937bc6423fa8477e`.
- Letti `docs/development/roadmap.md` e `docs/growth/pilot-first-revenue.md`. `STATUS.md` non era presente su `main` (GitHub 404): creato per rendere tracciabili le verifiche.
- Il catalogo HTML generato in `site/index.html` dichiara **18.396 offerte importate, 453 marche, 5 negozi**, con timestamp dei prodotti al 23 ottobre 2026, ore 06:49 UTC. Sono valori dichiarati dall'HTML nel repository, **non** misure di traffico, disponibilità attuale o dati verificati sul sito pubblico.
- I cinque negozi visibili nell'HTML includono Bauzaar, WebPet, Animaliapet, Isola dei Tesori e Paco Pet Shop. Arcaplanet non è confermato come fonte importata; non va aggiunto ai contatori né mostrato con prezzi ipotetici.
- Anomalia da indagare **nel generatore**, non da correggere manualmente sull'HTML rigenerato: la meta description della homepage elenca ancora quattro negozi, mentre il contenuto generato ne dichiara cinque. La home dichiara inoltre «Aggiornamenti ogni 6 ore»: la cadenza va confrontata con i run effettivi e l'età dei feed, senza dedurre che ogni fonte sia aggiornata a quella frequenza.
- `site/sitemap.xml` è un indice delle sitemap di pagine, categorie, guide, marche e prodotti; `site/robots.txt` dichiara la sitemap canonica. L'ultimo dato storico documentato in `docs/growth/pilot-first-revenue.md` è Search Console: sitemap riuscita, 304 URL rilevati al 23 ottobre; **rilevati non significa indicizzati**.
- `site/prodotto.html` ha `noindex,follow` e canonical senza parametri. È una scheda dinamica: prima di cambiarla, verificare le pagine prodotto statiche indicizzabili e il contenuto HTML effettivo.
- Tentativo di apertura pubblica via strumento web di homepage, robots e sitemap non riuscito per errore di accesso dello strumento. **Non è una prova di downtime**. Nessuna verifica browser end-to-end né conferma deploy Cloudflare in questa esecuzione.
- Nessun accesso verificato in questa esecuzione a dashboard ufficiali TradeTracker, Tradedoubler, AdSense o Search Console: **clic, ordini, commissioni e ricavi attuali non determinati**. Non interpretare un accesso assente come zero. Non utilizzare Gmail finché la connessione risulta in errore.
- Nessun click commerciale o pubblicitario, acquisto di prova, contatto esterno, modifica di credenziali o attivazione AdSense effettuato.

## Baseline storica, non aggiornata
La verifica del 23 ottobre riportata in `docs/growth/pilot-first-revenue.md` registra su TradeTracker 4 clic nel mese, 0 vendite e 0 € di commissioni; su Search Console 2 clic e 9 impressioni nel campione 17–20 ottobre. Non trasferire questi valori al periodo corrente senza nuova lettura dei pannelli.

## Prossimo intervento utile
1. Identificare il generatore della homepage e correggere alla fonte la lista negozi nei metadati solo dopo test di rigenerazione; non modificare file generati destinati a essere sovrascritti.
2. Verificare nei pannelli ufficiali Search Console le pagine effettivamente indicizzate, le query e gli errori di copertura; non reinviare la sitemap già accettata senza ragione.
3. Eseguire un test browser reale di ricerca → scheda → confronto, **senza aprire link commerciali**, e verificare il deploy Cloudflare. Controllare feed e formati prima di dichiarare equivalenze.
4. Verificare stato approvazioni Arcaplanet/zooplus e monetizzazione solo nei pannelli autorizzati; prima commissione da documentare con network, data, importo e stato.
5. Completare/verificare identità del titolare, privacy, cookie e consenso/CMP prima di ampliare tracking o abilitare AdSense. Mantenere indipendenza dell'ordinamento e disclosure affiliate.

Nessun ricavo reale attribuito verificato in questa esecuzione; nessuna condizione per arrestare il monitoraggio della prima commissione.
