# Verifica indipendente dei cinque negozi — 28 ottobre 2026

Controllati tutti i campi delle 18.292 offerte pubblicate del catalogo 14:42 UTC e 98 pagine originali (campione stratificato, ampliato a tutte le 62 incoerenze di peso Bauzaar). La verifica non è stata avviata da singoli esempi di prodotto. Le 98 letture hanno restituito HTTP200, ma gli esiti semantici sono distinti:

| Negozio | Pagine lette | Prezzo/stock della variante verificati | Inconcludenti |
| --- | ---: | ---: | ---: |
| Bauzaar | 69 | 69 | 0 |
| WebPet | 8 | 8 | 0 |
| Animaliapet | 7 | 7 | 0 |
| Isola dei Tesori | 6 | 6 | 0 |
| Paco Pet Shop | 8 | 4 | 4 |

Il campione non è una certificazione di tutte le pagine. I tre feed ufficiali sono stati riscaricati integralmente e confrontati con i record pubblicati: nessuna differenza di prezzo, stock o destinazione nelle rispettive offerte normalizzate. I feed Bauzaar e Isola espongono soltanto stock positivo nel recupero osservato; non è stato dedotto che l’intero negozio sia sempre disponibile. WebPet contiene soprattutto acquariologia e accessori: il basso numero di pesi alimentari non è da solo un guasto.

## Errori trovati e risolti

- Il registro FortiFlora richiedeva uguaglianza letterale del GTIN: il primo aggiornamento da feed a 13 cifre annullava il collegamento registrato a 14 cifre. Ora il confronto usa la rappresentazione equivalente; il test riproduce importazione dei due feed, riconciliazione della confezione e revisione.
- 62 pesi Bauzaar differivano fra unit_pricing_measure e titolo. Tutti i 62 sono stati verificati sulle varianti originali e corretti mediante evidenza vincolata all’ID esatto, prezzo della confezione, stock e barcode. Esempio: lettiera Natural Code 5 litri (4 kg) era registrata come 4,4 kg. Non si usa il peso di spedizione come peso netto.
- I titoli «85 gr — confezione da 24 pezzi» non avevano un peso totale riconosciuto. Ora la quantità di vendita esplicita viene calcolata; pesi multipli discordanti e quantità ambigue restano esclusi.
- Paco mancava dalla allowlist del controllo dei link. Aggiunti URL diretti esatti e test di copertura dei cinque negozi.
- Il feed Paco può avere un EAN diverso dalla variante predefinita della pagina. In quattro degli otto casi campionati questa identità non è verificabile. Non si sostituisce il barcode della variante con quello generico nello schema pagina. Confezioni non verificate non possono generare totali o carrelli stimati.

## Controllo permanente

`audit_store_integrity.py` verifica i campi di tutte le offerte e riserva una quota di pagine a ciascuno dei cinque negozi ad ogni ciclo. Selezione progressiva con priorità ai conflitti; esiti inconcludenti conservati come tali. Accessi diretti limitati, robots rispettato, niente redirect affiliati o carrelli reali. Il risultato è pubblicato in `data/store-audit.json` e nella pagina Correzioni; le discrepanze aperte producono warning nella CI.

Le prove del formato e del GTIN sono legate a titolo, ID, URL, marca, prezzo, stock e dati nativi; si riusano per massimo sette giorni e non modificano prezzo, stock o data del feed. Cambiamenti invalidano la prova. Il report delle pagine mostra gli esiti recenti entro 36 ore, con timestamp di ciascuna lettura. Il controllo indipendente non equivale al semplice successo dell’importazione.

Verifica locale: 118 test Python, 95 test Node e audit statico senza problemi. La prova mobile verifica anche l’accesso a ognuno dei cinque cataloghi e il blocco del carrello per varianti Paco non verificate. La CI ricostruisce i dati dal checkout e riproduce le evidenze senza rete; la rigenerazione produttiva recupera nuovamente i feed.
