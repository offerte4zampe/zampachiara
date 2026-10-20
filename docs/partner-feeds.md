# Official partner catalog ingestion

Prepared stores: Arcaplanet, L’Isola dei Tesori, zooplus. None is activated by this change. Access and field mapping must be verified with a real authorized export first. No credentials or raw private exports belong in this repository.

Normalize an authorized export to a private JSON file with:
- merchant_id: arcaplanet, isoladeitesori, or zooplus
- source_type: official_feed
- checked_at: actual ISO timestamp of the feed observation, timezone required
- offers: id, title, url (direct HTTPS product URL), price (EUR number), available (boolean explicitly provided by source)
- optional variant, brand, category, sku, gtin, weight_kg plus weight_source documenting explicit net package weight

Run `python automation/import_partner_feed.py /private/path/normalized.json`, then enrichment, history and page builders as in catalog.yml. Current importer accepts normalized JSON only; provider-specific CSV/XML downloads and mappings are not implemented until a real feed is available. Links remain direct until an approved tracking URL mechanism is configured. Feed URLs and tokens must never be exposed in source metadata.

Snapshot replacement removes obsolete offers from that merchant and retains other merchants. Invalid/empty/stale feeds fail before mutation. Regular catalog refresh preserves official partner snapshots with their original timestamps; UI flags stale prices and avoids shipping estimates. Do not refresh timestamps without retrieving data.

Amazon: generic search buttons removed. Restore product links only after verifying an exact ASIN/recipe/package mapping. Never populate prices or stock from search snippets. Official API access, license-compliant cache and expiry rules are still required before ingestion; Amazon is intentionally excluded from this importer and price history.

## Isola dei Tesori (20 ottobre 2026)
Campagna TradeTracker 31221 accettata per sito affiliato 518044, verificata nel pannello. Feed ufficiale 1618255 (7.223 prodotti al recupero), aggiornamento del fornitore giornaliero. Importazione programmata ogni sei ore; non prezzi in tempo reale. `automation/isola_feed.py` conserva link prodotto esatto, GTIN dichiarato, disponibilità e prezzo EUR. Peso netto soltanto dal formato esplicito nel titolo; litri e quantità ambigue non convertiti. Nessuna percentuale di sconto. Le condizioni aggregate di spedizione restano da verificare: deliveryCosts del feed non basta per modellare un ordine o una soglia gratuita.

Condizioni lette nel pannello: deep link e CSS consentiti; PPC non consentito; coupon soltanto forniti da network/merchant. Email marketing solo su richiesta con anteprima DEM approvata dal cliente: nessun invio autorizzato o attivato da questa integrazione. Non sono stati cliccati link tracciati per verificarli.

Il recupero iniziale contiene 2.747 URL multipack: esclusi perché titolo/GTIN del pezzo non dimostrano la base del prezzo per la quantità richiesta. Restano 4.476 offerte importabili. Non moltiplicare o dividere i prezzi per deduzione.
