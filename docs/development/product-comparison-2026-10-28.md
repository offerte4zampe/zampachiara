# Confezioni e confronto tra negozi — 28 ottobre 2026

## Problema e intervento
Il catalogo pubblicato del 28 ottobre alle 13:00 UTC conteneva FortiFlora Canine polvere 30 bustine da 1 g disponibile sia su Bauzaar (26,98 euro) sia su Isola dei Tesori (40,69 euro). Il peso Bauzaar era 1 g; il peso Isola non era riconosciuto e il feed Isola non dichiarava GTIN. Il confronto mostrava erroneamente il negozio come assente dal catalogo.

Il parser ora riconosce quantità esplicite nei due ordini, pezzi e compresse, senza usare il peso di trasporto. La rigenerazione ricalcola anche i vecchi pesi inferiti. Rispetto al catalogo di partenza: 36 pesi recuperati, 22 corretti, 27 rimossi perché ambigui. Nessun prezzo o timestamp delle offerte è stato cambiato. Sono presenti 280 gruppi tra negozi; il numero totale non è una misura sufficiente della qualità degli abbinamenti.

`reviewed-identities.json` collega soltanto le due schede FortiFlora Canine polvere 30 x 1 g revisionate. Il GTIN deriva dalla scheda Bauzaar, non da una lettura del barcode Isola. Provenienza e scadenza sono conservate nei dati e l'interfaccia distingue l'abbinamento revisionato. Titolo, URL, marca, peso, riferimento, codice discordante o scadenza impediscono l'applicazione. Chews, Plus, Feline e confezioni da 7 restano separati. Non è stato introdotto un abbinamento automatico per somiglianza.

Fonti di identità:
- https://www.bauzaar.it/products/purina-veterinary-diets-fortiflora-canine?variant=56820111606085
- https://www.isoladeitesori.it/prodotto/purina-proplan-fortiflora-probiotic-per-cani-30-pz-x-1-gr/000132103.html

## Interfaccia
I risultati confrontabili hanno una scheda per prodotto/formato con elenco sintetico di negozi e prezzi, un accesso al confronto completo e strumenti riferiti all'offerta selezionata. La scheda prodotto apre una tabella con prezzo, spedizione, totale, disponibilità e data. Le spese sconosciute non diventano zero. I dettagli per negozio restano disponibili. L'assenza di una corrispondenza certa non è più presentata come assenza dal catalogo del negozio; un link permette di cercare tra le offerte importate.

La struttura riprende i percorsi osservati su BauDeal e Trovaprezzi, mantenendo contenuti e grafica del progetto.

## Verifica
108 test Python, 93 test Node e audit statico delle 469 pagine senza problemi. Nuova regressione browser mobile per la presenza delle due offerte FortiFlora e la scheda raggruppata, nella CI delle pull request. Il browser locale non è installabile in questo ambiente: la verifica mobile viene eseguita in GitHub Actions prima del merge. Non è stata rivendicata una copertura completa dei cinque negozi: molti GTIN rimangono mancanti, in particolare WebPet e Paco.
