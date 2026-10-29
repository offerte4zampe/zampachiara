# Outbound redirects (JSON, independent of D1)

`/go/{percent-encoded offer_id}?from=product` reads the existing canonical route
and product shards. The only external target is `O4ZTrade.merchantUrl(offer)`,
shared with the merchant-choice UI. It preserves the feed URL byte-for-byte,
including affiliate parameters. No URL supplied by a request is accepted.
Current merchant-choice surfaces: canonical SSR, legacy product JS, basket,
and generated `prezzi-*` detail buttons (next catalog regeneration).
Editorial title links still lead to the internal product comparison.

GET/HEAD always issue 302, no-store, noindex, no-referrer. Unknown IDs cannot
identify a product, so return to /confronta-cibo. Known inactive/stale offers
return to their canonical product. Asset failure also returns internally.
Snapshots removed from route shards cannot recover a former product; no
untrusted fallback slug or URL is accepted. No merchant URL is fetched by the
redirect, so validation does not create affiliate clicks.

The existing opt-in command synchronizes localStorage with the host-only
Secure SameSite=Lax session cookie `__Host-o4z-statistics=yes|no`, Path=/.
No cookie means no statistics. GPC/DNT override consent. Revocation updates
both stores. JS disabled still navigates; only a previously set consent cookie
can authorize a server-side event. Cookie storage failure leaves navigation intact.

Only GET, explicit consent, no GPC/DNT and no prefetch create one event. HEAD
and inactive/unknown offers create none. `ctx.waitUntil` and a caught promise
isolate missing/throwing/rejected analytics bindings. No double browser event
is sent for /go/ links. Page source is an allowlisted label, not a full referrer;
it is client-declared and not suitable for billing or fraud-proof attribution.

Dataset: `offerte4zampe_outbound`, binding `OUTBOUND_CLICKS`.
Index: merchant_id; blobs 1..4: merchant_id, public product_id, public offer_id,
page type (home/catalog/product/basket/other); double1: price cents.
No IP, cookie value, visitor ID, search text or full URL is stored in this dataset.
Infrastructure security logging is distinct from application analytics.

## Limits and operating costs checked 2026-10-29

Official sources:
- https://developers.cloudflare.com/analytics/analytics-engine/get-started/
- https://developers.cloudflare.com/analytics/analytics-engine/limits/
- https://developers.cloudflare.com/analytics/analytics-engine/pricing/

Retention is service-controlled, three months. One point per valid consented
click, four blobs, one double, one index: well below 20 blobs/20 doubles/1 index,
16KB combined blobs, 96 bytes/index, 250 points/invocation.
Published free allowance: 100,000 points/day and 10,000 queries/day. Paid:
10m points and 1m queries/month included; overage $0.25/m points, $1/m queries.
Documentation currently says billing is not yet enabled; recheck before rollout
rather than assuming indefinite free use. No polling/query schedule is added.
For daily reports use at most one daily aggregate query and SUM(_sample_interval),
not COUNT(*), because Analytics Engine can sample. No reporting token is committed.

## Affiliate terms and images: rollout prerequisites

Public TradeTracker code of conduct defers campaign restrictions to each
campaign description. Its public website terms are not the publisher feed
license. These sources do NOT establish a blanket right to cloak/redirect
links or copy/rehost all product images:
- https://tradetracker.com/ee/code-of-conduct/
- https://tradetracker.com/it/terms-of-use/
- https://tradetracker.com/it/knowledge-centre/for-publishers/

Check authenticated campaign conditions for Bauzaar, Isola and Paco before
publishing merchant redirects. Do not treat this PR as verification of them.
Shopify's service terms concern the merchant/platform agreement and do not
establish a publisher image license: https://www.shopify.com/legal/terms
WebPet/Animaliapet require source-specific permission/terms review.
Image transformations also cache/copy content; the image pilot remains unenabled
until source permissions are established. No Images/R2 binding or cost is added.

## Validation

`node --test tests/test_outbound.mjs` checks exact target equality for EVERY
catalog offer and resolves every current offer through the actual JSON shards
using fixture clocks, without merchant requests. It separately covers consent,
privacy headers, expired/unsafe/unknown offers, HEAD, prefetch and failed telemetry.
`node --test tests/test_metrics.mjs` covers browser opt-in/privacy.
`python -m unittest discover -s tests` includes static navigation idempotence.
D1 stays JSON/shadow=false; no D1 credentials or remote staging run are involved.
