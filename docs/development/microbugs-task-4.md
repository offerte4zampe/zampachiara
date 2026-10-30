# Task 4 — Consistent display and small comparator fixes

Timestamp display is shared by browser and Worker via `trade.formatTimestamp`:
Italian day/month/four-digit-year and minute precision, Europe/Rome. Dates without
a recorded time retain date precision. Generated HTML receives the same formatting;
ISO attributes and JSON are preserved. Relative labels use Intl.RelativeTimeFormat
with numeric always, including singular `1 ora fa`.

Home totals and per-store counts derive from the same final snapshot after any
quarantine/normalization. The disabled sale filter is hidden both statically and
in the client. The obsolete sorting asterisk is removed if present. Per-store
history labels in canonical product pages use text rather than empty H3 headings.

Validation: 188 Python tests, 135 Node tests; 489-page static audit with no issues;
Wrangler dry-run succeeds. Regression tests cover Rome summer/winter offsets,
relative singular/plural, unchanged machine timestamps, idempotent HTML formatting,
and store totals matching the home count without mutating input snapshots.

No affiliate destination, tracking choice, D1/shadow flag or shipping rule changed.
