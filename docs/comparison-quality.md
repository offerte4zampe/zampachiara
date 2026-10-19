# Comparison quality

- Each regular import is followed by a bounded public-product-JSON inspection: at most 30 product URLs and about two minutes, an eight-second request timeout, robots checks and a cached one-week refresh target. Similar names only prioritize candidates; they never certify a match.
- Public `barcode` values must pass GTIN checksum/length validation, then are zero-padded to 14 digits. Cross-shop UI matches also require the same normalized brand and explicit net package weight. Recipe/label verification remains necessary. Missing/contradictory data is not filled from guesses.
- `automation/identifier-cache.json` stores only public merchant identifiers, shipping weights and source timestamps. No subscriber/customer data.
- `catalog-quality.json` states actual coverage; it is not a claim that the whole catalog has verified identifiers.
- Shipping quotes are estimates for quantities of ONE offer, not mixed baskets. Current rules only apply to standard Italian delivery. Unknown shipping weights, stale prices, ambiguous boundaries, conflicting merchant policies and special destinations suppress a quote. Shipping-weight data is never used as net weight for unit pricing. Rules expire after seven days until independently rechecked.
- Reference-price discounts exceeding 60% are not automatically highlighted. This is an anomaly filter, not proof of a valid previous selling price for the remaining products.
- Daily history stores observed low/high/latest price and latest availability for a maximum of 90 days. Retained stale catalog entries do not generate a new daily observation. Start date is the actual first run; no backfill.
- The site currently has three catalog sources. This does not guarantee that any particular product is available from all three. The target of 30 habitual products at three shops each has not been met by merely importing these catalogs. Expand approved feeds only with verified identifiers and sufficient overlap.

## Aggiornamento 19 ottobre 2026

Il comparatore raggruppa automaticamente solo offerte fresche (massimo 36 ore) con GTIN valido normalizzato, marca e peso netto coincidenti, presenti in negozi diversi. Il filtro `matched=1` limita la ricerca a questi gruppi. Non si usano nomi simili per certificare l'equivalenza. I negozi sono ordinati per disponibilità e prezzo prodotto; un totale di spedizione sconosciuto resta esplicito.

I clic TradeTracker della campagna Bauzaar 16143 per il sito 518044 sono riconosciuti dalle statistiche facoltative; vengono inviati solo evento e negozio, senza URL o ricerca. Questo non rende disponibili utenti unici o vendite: la consultazione del traffico Cloudflare via API richiede ancora un collegamento autenticato.

Il feed prezzi Bauzaar resta ufficiale. I pesi di spedizione vengono recuperati separatamente dalla variante del catalogo pubblico (campo grams), con cache rinnovata ogni giorno e scadenza massima di sette giorni. Non sostituiscono prezzo, disponibilità, GTIN o peso netto del feed. Se il dato manca, è scaduto o supera i limiti della regola, il totale non viene calcolato.

Una scheda statica il cui prodotto non compare più nel catalogo viene trasformata in avviso senza prezzo né disponibilità, esclusa dall'indicizzazione e rimossa dalla sitemap. I dati statici oltre 36 ore non mostrano un pulsante di acquisto o disponibilità attuale.

Gli spazi sponsor vuoti in home e prima dei risultati restano nascosti; le campagne effettivamente attive continuano a essere visualizzate con etichetta pubblicitaria.
