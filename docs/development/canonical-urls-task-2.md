# Task 2 — Clean internal URLs

Reconciled with PR #17: its 30-item prerender and on-demand full-catalog loading
are retained. This task completes redirects for the remaining HTML pages, cleans
all built internal links and extends direct canonical navigation to basket/favourites.

The Worker redirects GET/HEAD requests for `.html` pages to clean paths with 301,
retaining the query string. `/prodotto.html` keeps its legacy ID resolver; Google
verification files remain assets. Wrangler routes `.html` requests through the Worker.

`automation/clean_urls.py` runs after shared-layout inclusion at deployment. It
cleans internal href/action attributes, resolves exact legacy product IDs from
the catalog, and replaces old GTIN page links with their canonical product route.
External merchant links are preserved, including query bytes after HTML decoding.

Conservative interpretation: `url` is an existing merchant destination used by
outbound and affiliate logic, so it is retained. The separate `product_url` field
stores the internal canonical route. All 18,361 offers in this snapshot have a
canonical route. Catalog, home, suggestions, basket and favourites use the slug
rather than constructing legacy ID URLs. Unknown IDs keep the legacy resolver;
missing or unsafe slugs in client data lead to the comparator, never a guessed item.

Validation: 180 Python tests and 132 Node tests pass. Post-build static audit:
489 pages, zero issues; no internal href/action contains `.html`. Second inclusion
run modifies zero pages. Before publication, live /index.html and
/confronta-cibo.html used 307; post-publication checks must verify 301 and direct
product responses. No affiliate, tracking, D1/shadow or shipping semantics changed.
