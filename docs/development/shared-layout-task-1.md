# Task 1 — Shared navigation, footer and disclosure

The authoritative chrome lives in `automation/partials/header.html` and
`automation/partials/footer.html`. `automation/apply_navigation.py` includes it in
all static HTML pages, recursively, before Cloudflare uploads the assets.
Existing catalog and coupon workflows also run the same inclusion step.
The canonical product Worker inherits the built `/prodotto` template.

`automation/stores.json` supplies the current affiliate merchant names and network.
The Amazon disclosure remains in the shared footer. Current TradeTracker partner
lists in page copy are normalized from the same configuration. Historical start
dates remain distinct from the current partner list.

Build output is intentionally not committed: the deploy build applies these
partials to all pages, including pages generated after this PR. Source HTML is
therefore not the final deployed HTML. Run `python automation/apply_navigation.py`
before inspecting or serving the static checkout.

Validation on the 2026-10-30 snapshot:

- Python: 175 tests passed.
- Node: 127 tests passed after the existing build preparation step.
- Static audit after inclusion: 489 pages, zero issues.
- All 489 built pages share the same header (apart from current-page indication)
  and complete footer, with Guide, Marche, Confronti and Registro correzioni.
- Inclusion is idempotent; Google verification token is untouched.
- Product breadcrumb points to `/prodotti`; internal links have no external arrow.
- Affiliate destinations, tracking logic, D1/shadow flags and shipping rules are unchanged.

No merge or production deployment performed as part of this task.
