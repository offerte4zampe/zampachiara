# D1 shipping: staged runtime verification

Production remains JSON (`SHIPPING_RULES_SOURCE=json`, `SHIPPING_SHADOW=false`). No production D1 binding is provisioned by this change. The flag currently applies to canonical product pages rendered in the Worker; client-side basket tools still load the JSON snapshot.

## Resources and migrations

`wrangler.staging.jsonc` is intentionally separate from production's existing `wrangler.jsonc`. It has a dedicated Worker `zampachiara-d1-staging`, database `zampachiara-shipping-staging`, binding `SHIPPING_DB_STAGING`, and no production routes. The all-zero UUID is local-only; the remote runner resolves/creates that exact named staging database and writes an ignored runtime config. It never adds a binding to production.

`worker/staging/migrations/0001_shipping_rules.sql` is the reviewed shipping schema. Apply it with Wrangler migrations; the runner uses `wrangler d1 migrations apply`, not manual schema execution. A test guards against drift from the reviewed SQL.

Install Wrangler 4.154.0, then run:

```sh
python automation/verify_d1_staging.py --wrangler /path/to/wrangler
```

This starts local workerd, loads the seed through a D1 `batch()` inside the staging Worker, and writes `staging-reports/local-shipping-report.json`. Local metrics are explicitly labeled local; they do not establish remote D1 performance or compatibility.

## Remote execution

The GitHub workflow **D1 shipping staging** has a manual `remote=true` option. It uses the `cloudflare-staging` environment and requires `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN` there. The account must allow creating a D1 staging database, applying its migrations, and deploying the separate staging Worker. Configure credentials through the secret store, never through repository files or chat. No token is included in reports.

Alternatively run the same script with `--remote` in an authenticated environment. It stops before making changes if account credentials are missing; remote mode never silently becomes a local test. The staging diagnostic endpoints require a freshly generated Worker secret; production has no diagnostic endpoint. The runner does not delete the staging resources after verification so operators can inspect them.

The remote report contains:

- Seed row counts (five shops and five rules), and the actual sum of `meta.rows_written` from the binding batch. Explicit SQLite `BEGIN/COMMIT` wrappers are not passed to D1.
- 610 fixture combinations calculated *inside the Worker* using rows read from its actual binding. Reference times derive from the unchanged source verification dates; the report never presents historical fixtures as current merchant observations.
- `meta.rows_read` for the rule lookups of a five-shop product request, plus `EXPLAIN QUERY PLAN` so index use is verified independently from the billing counter. The optimizer may choose the equivalent UNIQUE index on `(shop_id, zone, valid_from)` instead of `idx_ship_shop`; either indexed search is valid, a full rule scan is not.
- Actual capability probes for CHECK constraints, a generated column with an index, triggers, and FTS5 with the trigram tokenizer. FTS availability is recorded, not assumed. `sqlite_version()` may be forbidden through the binding; that diagnostic is optional and is never used to infer feature availability. Temporary probe tables are removed; the five shipping rules remain.

## Fallback, shadow, and rollback

`worker/shipping-source.mjs` deduplicates shop IDs and issues parameterized queries using ISO UTC timestamps. JSON is used without a D1 query unless D1 or shadow was explicitly enabled.

- `SHIPPING_RULES_SOURCE=json`: JSON results are displayed.
- `SHIPPING_SHADOW=true`: query both sources, keep the selected visible source, log only quote differences as `shipping_shadow_difference`. Do not log the user's search, identity, page URL, or product title.
- `SHIPPING_RULES_SOURCE=d1`: use adapted D1 rules. Binding/query failures, invalid returned rows and missing rules fall back to JSON and emit `shipping_d1_fallback`.
- Expired or uncertain *valid data* stays uncertain. It does not fall back to a more favorable older rule.
- Rollback is setting `SHIPPING_RULES_SOURCE=json`; set `SHIPPING_SHADOW=false` as well to stop all D1 reads.

Do not enable production D1 until a remote report passes, and shadow differences have been reviewed. The default remains JSON until that separate activation.
