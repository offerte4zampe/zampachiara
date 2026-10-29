# Multishop recovery, 2026-10-29

Snapshot generated 2026-10-29 around 17:03 UTC, all five sources reported ok.
Source counts can differ from the usable catalog after quarantine/deduplication.
Using exactly the same snapshot clock:

| Measure | Before | After explicit brand aliases |
| --- | ---: | ---: |
| Active canonical products | 16,796 | 16,709 |
| Products in at least two verified stores | 420 | 504 |
| Multishop share | 2.50% | 3.02% |

Ten exact, reviewable brand labels in automation/brand_aliases.json cover only
subline/syntax differences. A shared checksum-valid GTIN and identical verified
selling quantity remain mandatory. Aliases alone never join products; arbitrary
prefix matching and fuzzy joins are not used. Corporate owner/product brand pairs
such as Askoll/Ciano, Elanco/Advantix and Camon/Orme Naturali remain separate.
Feed brand labels stay on offers for provenance; canonical products use the
reviewed brand. This is not permission to equate different recipes or formats.

Legacy canonical URLs remain in the registry. When every former offer is still
present and resolves to one current product, the old page issues 301 to the
current canonical URL. Removed or split offers keep an unavailable archive;
no redirect is guessed. The target is validated locally, never request supplied.

## Independent all-store field inventory

Counts are over 18,356 usable snapshot rows, not live manual checks of each page.
Missing GTIN and unverified quantity can overlap and should not be added.

| Store | Offers | Missing valid GTIN | Unverified quantity | Offers in multishop products after fix |
| --- | ---: | ---: | ---: | ---: |
| Bauzaar | 7,199 | 445 | 0 | 467 |
| WebPet | 1,946 | 1,806 | 0 | 30 |
| Animaliapet | 3,993 | 2,562 | 0 | 269 |
| Isola dei Tesori | 4,039 | 2,709 | 0 | 177 |
| Paco | 1,179 | 995 | 995 | 83 |

Zero unverified quantities does not imply an explicit mass is present. Many rows
have only a sales unit. The generated product-coverage.json now exposes these
blockers and active/multishop offer counts for each store on every import.

The public Shopify barcode enrichment previously skipped rows without mass.
It now permits available accessories, pieces and volume products from shared
brands to enter the bounded robots-respecting inspection queue (1,195 Animalia
and 273 WebPet candidates in this snapshot). This is lookup eligibility, NOT
newly verified barcodes or matches. Existing request/time budgets, cache expiry,
variant-specific identifiers, checksum validation and quarantine remain intact.
Official feed rows are not overwritten by this enrichment.

Next evidence priorities: missing native GTINs in WebPet and Isola; Paco exact
selling-variant verification (995 uncertain rows must not be matched by title).
Feed success proves an import happened, not every merchant page is correct.

## Outbound verification boundary

/go is deployed and the dataset binding was enabled by the owner. Public page
inspection confirmed the new links and robots rule. Tests cover opt-in/revocation,
GPC/DNT, absent/failed binding and exact affiliate targets over all snapshot rows.
Actual dataset ingestion requires an authenticated Analytics Engine query; no
read token/session is available in this task. Do not claim receipt of real events
from configuration or unit tests, and do not generate affiliate clicks as a test.
D1 remains JSON/shadow=false and is separate from this work.
