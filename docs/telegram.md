# Telegram channel integration

Destination is pinned to @sconti4zampe. The secret TELEGRAM_BOT_TOKEN and text
TELEGRAM_CHANNEL_ID must already exist in Cloudflare. keep_vars preserves
existing dashboard variables; no secret belongs in source or CI output.

Cloudflare's existing Git deployment provisions the SQLite Durable Object binding
TELEGRAM_PUBLISHER (migration telegram-v1). No separate paid service is required.
The scheduled handler checks every 15 minutes. First run sends exactly one
labelled test message; ordinary posts start on a subsequent day at 09:15
Europe/Rome, accounting for daylight saving. Two days out of three prefer a price report from home.json, requiring a successful
source and available exact-format price checked within 24 hours. Reports state
source, observation time and excluded shipping; they do not claim discounts.
Products are linked directly on the comparator and never reposted automatically.
Other days use three original Telegram summaries of existing guides; guides are
also the fallback if no fresh eligible offer exists. Empty queues remain silent.
No claimed discounts, prices or stock are invented. Facebook/Instagram/Metricool
are not changed. New queue entries require reviewed source changes and unique
stable IDs; never change an ID simply to resend a post.

GET /api/telegram/status is a read-only operational check returning only version,
configuration boolean, test status and public test message ID. All other methods
on that route return 405. There is NO HTTP publishing endpoint. Only the internal
Durable Object binding can tick publishing. The public status route cannot
trigger a send or expose the token, queue bodies or history.

Durable Object storage keeps post:<id> records with attempt/finish dates, outcome,
attempt count and Telegram message ID. Inspect these through authenticated
Cloudflare Durable Object tooling. Console events contain only post ID, outcome
and public message ID. Never log exceptions, Telegram response descriptions or
request URLs (the Bot API URL contains the token).

The durable send reservation is written before contacting Telegram and survives
restarts/deploys. A completed or uncertain attempt is never resent automatically.
Network timeouts, malformed responses and 5xx stop the queue for manual review:
Telegram has no idempotency key, so blindly retrying can duplicate a delivered
message. Only explicit 429 rejections are retried after retry_after, at most four
attempts. Retries wait for the next 15-minute cron check after retry_after. Price reports
that become older than 24 hours while waiting expire without being sent.
Before resuming a halted record, reconcile it with the channel. Do not delete
persistent history or recreate the object with a different name.

Pause: remove the cron trigger through a reviewed configuration change, or remove
the bot's permission to post. Do not remove the Durable Object migration/history.

Before Node tests: `python automation/check_d1_activation.py --prepare-build`.

Validation: node --test tests/test_telegram.mjs tests/test_metrics.mjs
 tests/test_product_preview.mjs tests/test_notification_plan.mjs
All Telegram tests replace fetch with mock transport and never send real messages.
