# Task 6 — Image layout, fallback and licensed local-cache pipeline

**Partial: local rehosting remains disabled for all five stores.** Public sources
reviewed on 30/10/2026 do not establish store-specific permission to retain and
convert product photos. General affiliate promotional access is not treated as
proof of local-cache permission. No product photos have been downloaded or
converted for publication. Existing remote images remain visible until explicit
permission is verified, as required by the supplied conservative instruction.

The per-store review lives in `automation/image-rights.json`. Sources include:

- https://tradetracker.com/it/tradetracker-publisher-tips/
- https://tradetracker.com/it/terms-of-use/
- https://www.bauzaar.it/products
- https://www.webpet.it/policies/terms-of-service
- https://www.animaliapet.eu/pages/condizioni-di-vendita
- https://www.isoladeitesori.it/condizioni-generali-di-vendita.html
- https://www.pacopetshop.it/en/

`cache_product_images.py` requires verified evidence and explicit allow_cache,
uses allowlisted HTTPS image hosts (including redirects), bounds input size,
and creates 400×400 WebP images with preserved alpha. Merchant and affiliate
URLs remain unchanged. The catalog workflow runs this step and publishes the
manifest and any licensed cache files. Browser/product templates can consume
image_local; static markup also checks the manifest and actual local file.

All product markup gets width/height, alt, lazy loading and async decoding.
Dynamic cards have the same image box and a local SVG failure fallback. The
preconnect list follows the CDNs actually used on each page. The measured home
LCP is the H1, so no arbitrary product image receives fetchpriority high.

Before-task PageSpeed evidence is in docs/audits/2026-10-30/before-task-6-7.json:
home 98, LCP 906 ms, CLS 0; comparator 100, LCP 905 ms, CLS 0. No CrUX/INP data.
Product report was launched but its metrics could not be read due to a browser
usage-limit approval failure; values are deliberately absent.

Validation: 191 Python and 135 Node tests passed; 499-page audit has zero issues.
Tests prove that unverified permissions cause zero downloads and a synthetic
licensed fixture converts to a 400-square WebP. No real store cache is enabled.
