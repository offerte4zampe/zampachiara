# Full catalog characteristic matching

Every catalog offer is evaluated on each import, without a sample or a cap on
candidate results. On the 18,356-row replay: 8,778 rows have enough explicit
characteristics; 9,578 remain insufficient. Eleven offers without GTIN attach
through exact characteristic keys, giving 517 multishop products versus 508.
Ten multishop products include characteristic matching (one was already multishop).
This is a snapshot replay, not a guaranteed future total.

`automation/name_matching.py` requires a known canonical brand, verified explicit
mass/volume/pieces, identical selling quantity, declared pieces and multipack count,
and identical sets of normalized name tokens after limited grammar/feed cleanup.
Generic brand/adult/recipe alone is insufficient. Important name words remain,
including recipe, age, diet/line and species. No edit-distance threshold, similarity
percentage or probability authorizes a merge. Request/merchant URLs and prices
have no role in identity. Animal weight threshold labels are excluded.

When a group has exactly one valid GTIN identity, only missing-code offers may
attach. A missing-code row can never bridge conflicting valid GTINs. With no code,
a deterministic characteristic identity is generated. GTINs remain on their
source offers; missing barcodes are never copied or fabricated. `offer_matching_method`
records provenance; product methods distinguish GTIN, characteristic and mixed.

All characteristic/mixed products are disclosed in SSR and catalog cards, are
noindex until independently verified, and have no confidence percentage.
`gtin_multi_shop_products` and `characteristic_multi_shop_products` are separate
metrics. Overall counts are not presented as all-GTIN verified comparisons.
Unknown format, low-information names, uncertain merchant quantities and conflicts
remain separate. Existing candidate report truncation is removed. Exact token
matching is intentionally stricter than fuzzy similarity; the entire catalog is
processed even when an offer cannot safely be attached.

Old internal product URLs retain the existing unambiguous migration redirects.
Shipping uses unchanged per-offer rules and quantity checks. D1 remains disabled.

Tests cover missing-code pairs, unique-code attachment, conflicting GTINs, different
recipe/age/format/brand, unknown quantities, generic titles, canonical URL stability,
SSR disclosure, browser grouping and expiry. No artificial affiliate clicks or new
paid services are introduced.
