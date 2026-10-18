# Cloudflare analytics: read-only connection

Implemented: environment-authenticated GraphQL reader (`automation/read_analytics.py`). Not authenticated or live-tested yet. No workflow, public endpoint or automatic report publication is enabled. Do not run the reader in public Actions logs.

Create a custom Cloudflare token:
- Zone → Analytics → Read
- Zone resources: Include → Specific zone → offerte4zampe.it
- No DNS edit, Workers edit, account-wide administration, or Global API Key.
- Record the zone ID from the site's Overview (32 hexadecimal characters).

Save token as a protected secret named CLOUDFLARE_ANALYTICS_TOKEN and zone ID as CLOUDFLARE_ZONE_ID. Never paste a token in chat, commit it, put it in a URL or pass it on a command line. A securely connected runtime must expose these values as environment variables before the reader can run.

Run locally in that authenticated runtime: `python automation/read_analytics.py 2026-10-18`. The date is in Europe/Rome and today is partial. Output distinguishes HTTP requests from Cloudflare visits, states possible adaptive sampling and does not infer unique human visitors, clicks, sales or bot exclusion. Empty/missing/error responses never become zero traffic. Dataset availability and plan permissions require a first live test.

This alone does not give the assistant ongoing API access: a secret-enabled execution connection and private report retrieval must still be configured. Do not claim analytics is active before an authenticated query succeeds.

Official references:
https://developers.cloudflare.com/analytics/graphql-api/tutorials/end-customer-analytics/
https://developers.cloudflare.com/observability/logs/datasets/
