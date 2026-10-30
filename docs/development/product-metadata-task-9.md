# Task 9 — nomi, title e description prodotto

Il normalizzatore elimina quantità adiacenti ripetute anche con separatori e spazi diversi (`15 kg · 15kg`). Il confronto con la variante riconosce la stessa quantità senza aggiungerla una seconda volta. Identità, raggruppamento e registro degli slug restano invariati.

Un formatter condiviso da Worker e resolver legacy mantiene il nome completo nell'H1 e costruisce title entro 60 caratteri, con nome breve, formato e suffisso `Prezzo e storico`. Il suffisso del sito non viene aggiunto una seconda volta. La description usa il prezzo minimo tra le offerte disponibili mostrate e il relativo prezzo unitario quando verificato; con un solo negozio dice `Prezzo rilevato`, senza presentarlo come confronto.

Verifiche: 196 test Python, 145 test Node; campione dei 50 nomi attivi più lunghi con title entro 65 caratteri; nessuna fusione tra quantità diverse; escape dei nomi ostili e test esistenti del Worker conservati. Formatter caricato una volta prima del client legacy. Build e audit verificati prima della pubblicazione.

File: normalizzatore in `automation/build_product_catalog.py`, formatter `site/assets/product-metadata.js`, client `site/assets/product.js`, Worker canonico e preview, hook `automation/apply_product_metadata.py`, workflow e test dedicati. I nomi canonici negli snapshot saranno rigenerati dalla pipeline catalogo; il Worker applica subito la pulizia alla visualizzazione dei dati già pubblicati. Prezzi, URL commerciali, tracking, D1/shadow e regole di spedizione non cambiano.
