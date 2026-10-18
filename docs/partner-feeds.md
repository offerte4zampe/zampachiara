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
