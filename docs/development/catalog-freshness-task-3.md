# Task 3 — Source freshness and Isola feed recovery

Cause reproduced on 30 October 2026: the official TradeTracker feed contained
4,972 products, of which one had an empty availability value. The strict
normalizer raised `ValueError: Unknown availability` and the running catalog
workflow retained the previous 4,039 offers. The schedule was active: GitHub
run 41060331031 completed and logged stale Isola data with ValueError.

The importer now excludes the single unknown-stock product and records the count;
all existing campaign, destination, variant and currency validations remain.
A live import using this fix returned 2,471 eligible offers and excluded one for
unknown availability. Existing multipack exclusions account for the remaining
records: no new assumptions about price/pack quantities were introduced.

Source checked_at is the maximum observed offer timestamp, with attempted_at
separate. Failed imports cannot advance the age of retained offers.
Home selections exclude observations older than 12 hours, in Python and JS.
The comparator includes a static per-source warning plus client-side age refresh,
and badges on individual cards and grouped store summaries. Static catalog cards
also label observations beyond 12 hours. Missing/future dates are marked unknown.

Validation: 184 Python tests and 133 Node tests pass. Tests reproduce an old
13-hour observation with a current failed-fetch timestamp, banner visibility,
home exclusion, catalog badge and the one-product availability failure.
Build audit: 489 pages, zero issues; no stale featured offer in generated home.
The deploy build recalculates freshness without requesting external feeds.
Affiliate URLs, D1/shadow, consent and shipping calculations are unchanged.
