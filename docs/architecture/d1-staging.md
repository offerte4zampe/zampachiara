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

## Activation barriers and explicit remote status

The runner validates exact names, not merely a `-staging` suffix. Before migration, deployment and seed it re-reads the isolated runtime configuration and resolves D1 metadata with `wrangler d1 info`; the actual database name and UUID must match the intended staging resource. The returned Worker URL must have the exact staging Worker name. A mismatch aborts before the next operation.

The remote job checks credentials before any Wrangler operation. Missing credentials produce `remote-staging NON eseguito: credenziali assenti` in the Actions summary and fail the job. An always-running status job also distinguishes remote success from skipped/not-requested and failure. A green local job or green overall run with remote skipped is not remote evidence.

The repository no longer contains a positive/negative proof record. Only the successful remote workflow emits `remote-d1-attestation.json`, included in the immutable Actions artifact. It records the run ID, checked-out commit SHA, SHA-256 of the migrations/seed/verification inputs, actual verified database UUID, resource names and UTC verification time. A local execution cannot produce accepted remote evidence.

To inspect an actual successful remote run for the current D1 input version:

```sh
python automation/check_d1_activation.py --verify-run RUN_ID
```

The validator reads the GitHub run, latest jobs and artifact metadata through the API. It requires the exact workflow, manual dispatch on `main`, successful run and actually executed successful `remote-staging`. It checks the downloaded archive against GitHub's SHA-256 digest, then checks the artifact run ID, branch, original SHA and resource identity. For newer builds, GitHub’s compare API must confirm that the attested SHA is an ancestor; the current scoped input hash must still match. Redirected artifact downloads do not receive the GitHub credential. Repository proof files and tracked generated attestations are rejected.

Wrangler's production pre-build hook always runs the same validator with `--prepare-build`. Without `SHIPPING_D1_REMOTE_RUN_ID` it generates a denied-by-default build file under ignored `worker/generated/`; with a run ID it regenerates that file exclusively from validated API/artifact evidence. It never trusts a hand-edited generated file. No source commit is created to record success, avoiding a circular change of commit SHA.

The Worker requires API-verified ancestry and a matching scoped input hash before honoring D1/shadow flags. Both SHAs remain recorded as provenance; equality of the overall commit SHA is no longer required. The CI activation gate independently performs the API verification. Enabling either flag in the repository without valid evidence fails the gate. If runtime flags are changed without a validated build, JSON remains selected and no D1 query runs.

**Scoped hash and ancestry:** catalog-only commits can reuse a still-available successful remote attestation when GitHub confirms ancestry and the input fingerprint is unchanged. Divergent history or a changed scoped input blocks D1/shadow. The scope includes both Wrangler configurations, migration/seed SQL, the seed generator, shipping rules (the explicit `site/data/` exception), shared shipping calculations, D1 adapter, Worker routing/rendering and verification code/workflows. Catalog snapshots, observed price history and the product registry are excluded. The fingerprint does not rely on GitHub's truncated changed-file listing.

**Retention:** the artifact must be unexpired and downloadable. An expired flag, past expiration timestamp or HTTP 410 reports **“Attestazione scaduta”** and requires a new remote run. A missing/deleted artifact reports that evidence is unavailable; it is never silently treated as valid. Metadata must bind the artifact to the same `run_id`, `main` and attested SHA, in addition to the JSON record and archive digest.

## Infrastructure versus catalog imports

This attestation has scope `shipping-infrastructure-v1`. It establishes the behavior of the shipping schema, seed, adapter and runtime. It is not evidence that a particular catalog snapshot was imported correctly.

When `product`/`offer` imports are introduced, each import run must produce its own separate result: source snapshot hash/time, run ID, target database UUID, inserted/changed/unchanged/rejected row counts, eligibility/aggregate checks, JSON equivalence and actual `rows_written`/`rows_read`. A successful infrastructure attestation cannot replace these per-import checks, and a successful catalog import cannot authorize infrastructure changes. Those imports and their report format are not activated by this change.

Token and environment configuration remain operator actions: a short-lived staging token with D1 Edit and Workers Scripts Edit, environment `cloudflare-staging` with required reviewers, and manual workflow dispatch. Do not reuse this token/environment for production. A separate Cloudflare account is the stronger optional isolation; software name guards do not narrow an account-wide token's permissions.
