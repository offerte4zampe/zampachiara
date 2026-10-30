# Task 5 — Home copy

The requested phrase appears in the pet sticker beside the hero in the current
layout. It now reads `Il loro preferito, al prezzo giusto.` without replacing the
current main H1. The shipping-exclusion sentence remains once beneath the offers
section title and once in the shared footer. Individual home cards retain unit
prices but omit the repeated shipping sentence, in both HTML and hydration.

The navigation pass also handles the existing nested sticker arrow: internal
links no longer use the external-opening glyph; external links are preserved.
The footer records this editorial revision as 30/10/2026.

Validation: 188 Python tests and 135 Node tests pass; post-build audit of 499 pages
reports zero issues. Built home has exactly two occurrences of the full disclosure
sentence (section and footer), no old phrase and no repeated shipping note in
featured cards. No affiliate destination, tracking, D1/shadow or shipping rule changed.
