# Shipping rules: staging migration

The live comparator still uses JSON. No D1 binding, database, or remote migration is activated by these files.

- `worker/schema/0002_shipping_rules.sql`: versioned rules, constraints and overlap guards.
- `automation/build_shipping_seed.py`: JSON-to-row conversion; rejects unmapped fields, imprecise base units and overlapping intervals. It never refreshes verification dates.
- `worker/seeds/shipping-rules.sql`: generated, idempotent seed using UPSERT, preserving rule primary keys.
- `O4ZTrade.shippingRulesFromRows(rows, now, zone)`: converts selected database rows to the existing input format. It does not calculate shipping; both browser and Worker continue to call `O4ZTrade.shipping()`.

The original JSON had no explicit expiry: `trade.js` previously used seven days. That same period is now declared as `verification_max_age_days: 7`, and `verified_until` is set from the original observation date, not the generation date. The former seven-day fallback remains only for older cached payloads. Expiry for rows loaded from D1 comes exclusively from the row.

## Local validation

```sh
python automation/build_shipping_seed.py
python -m unittest discover -s tests
node --test tests/test_*.mjs
```

The equivalence test covers 610 combinations across all five shops, including threshold ± one cent, exact thresholds, known/unknown/over-limit weight, multiple packs, special territories and verification expiry. Additional tests load the actual SQL seed into SQLite, select the stored rows and send them through the same pricing function. Future and ended validity intervals are excluded; a newly valid uncertain rule never falls back to a more favorable older rule.

## Staging sequence

1. Apply the schema to an isolated SQLite/D1 staging database; load the generated seed.
2. Query current rows with bound ISO UTC timestamps, including `valid_from <= now`, `(valid_to IS NULL OR valid_to > now)`, and the requested zone. For a single shop use `ORDER BY valid_from DESC LIMIT 1`. Join `shop.name AS shop_name` when rendering.
3. Pass the rows to `shippingRulesFromRows`, then call the existing `shipping` function. Unknown fees remain unknown; never coalesce them to zero.
4. Before inserting a new version, close its predecessor with a matching `valid_to` in the same transaction. Python validation catches overlaps within the incoming batch; SQL triggers also reject overlaps against existing rows. Identical boundary endpoints are allowed.
5. Repeat the parity matrix against rows read from actual D1 staging before adding any production binding. Local SQLite parity does not establish D1 deployment compatibility.

No SQL total-price calculation is introduced. The SQL tables only store observed policy data and validity intervals. Animaliapet remains uncertain, with null fee and threshold. Bauzaar, Isola and Paco retain unknown behavior at the exact free-shipping threshold.
