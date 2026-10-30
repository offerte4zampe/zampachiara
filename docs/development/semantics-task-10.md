# Task 10 — heading e storico accessibile

I nomi delle card sono H3 sotto un H2 di sezione, inclusa l'offerta in evidenza della home. La build rimuove heading vuoti e salti nel main. Il footer condiviso usa H2 su tutte le pagine, preservando tipografia e identità del partial; non viene normalizzato in modo diverso a seconda della pagina.

Il grafico canonico a 90 giorni compare solo con più di 30 date osservate. Anche i grafici estesi del resolver legacy rispettano la soglia; la tabella rimane sempre disponibile. L'aria-label degli SVG include minimo, massimo e media delle osservazioni effettive, oppure dichiara che la media non è disponibile. Nessun prezzo viene ricostruito per date mancanti.

FAQ della home già in details/summary/p; pulsante menu già dotato di aria-expanded, aria-controls e nome accessibile; marker del calcolatore già accompagnati da Prodotto A/B: conservati e verificati. La correzione concorrente del menu mobile e i suoi test sui tocchi rimangono intatti.

Validazione locale: 198 test Python, 146 test Node; controllo 772 pagine con un H1, nessun salto o heading vuoto, nessun nome card H2 e un solo footer condiviso; audit statico e build Wrangler. Test dedicati verificano esattamente le soglie 30/31 date, medie osservate e idempotenza delle trasformazioni.

File: generatori home, client home/prodotto/storico, Worker canonico, partial footer e CSS, automation/apply_semantics.py, workflow/build e test dedicati. Prezzi, link affiliati, consenso, D1/shadow e regole di spedizione invariati.
