#!/usr/bin/env python3
"""Build a conservative weekly newsletter from current catalog data; no invented discounts."""
import datetime as dt
import gzip
import json
import os
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "site/data/catalog.json.gz"
OUTPUT = ROOT / "newsletter-approved.json"

def build(now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    if not CATALOG.exists():
        raise ValueError("Catalog missing")
    catalog = json.loads(gzip.decompress(CATALOG.read_bytes()))
    generated = dt.datetime.fromisoformat(catalog["generated_at"].replace("Z", "+00:00"))
    if generated.tzinfo is None or generated > now or now - generated > dt.timedelta(hours=12):
        raise ValueError("Catalog is stale or has invalid timestamp")
    seen = set()
    offers = []
    for o in catalog.get("offers", []):
        if not o.get("available") or not o.get("weight_kg"):
            continue
        if not o.get("title") or not o.get("merchant") or not o.get("url"):
            continue
        url = str(o["url"])
        parts = urlsplit(url)
        if parts.scheme != "https" or not parts.hostname or parts.username or parts.password:
            continue
        checked = o.get("checked_at")
        if not checked:
            continue
        try:
            checked_at = dt.datetime.fromisoformat(checked.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            continue
        if checked_at.tzinfo is None or checked_at > now or now - checked_at > dt.timedelta(hours=12):
            continue
        try:
            price = float(o["price"])
            weight = float(o["weight_kg"])
        except (ValueError, TypeError, KeyError):
            continue
        if not (0 < price < 100000 and 0 < weight < 100):
            continue
        key = (str(o["title"]).casefold(), str(o.get("variant", "")).casefold())
        if key in seen:
            continue
        seen.add(key)
        offers.append({
            "name": str(o["title"])[:180],
            "format": (str(o.get("variant") or "")[:80] or f"{weight:g} kg"),
            "price": f"{price:.2f} €",
            "shop": str(o["merchant"])[:100],
            "url": url,
            "unit_price": price / weight
        })
    offers.sort(key=lambda x: (x["unit_price"], x["name"]))
    selected = offers[:5]
    if len(selected) < 3:
        raise ValueError("Insufficient fresh available products; fail closed")
    result = {
        "verified_on": now.date().isoformat(),
        "subject": f"Offerte da fiutare · {now:%d/%m/%Y}",
        "offers": [{k:v for k,v in o.items() if k != "unit_price"} for o in selected],
        "selection_note": "Products selected by lowest unit price, not claimed discounts. Catalog timestamps checked, merchant links not live-verified."
    }
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result

if __name__ == "__main__":
    try:
        result = build()
        print("Prepared", len(result["offers"]), "fresh catalog offers (not live merchant verified)")
    except (ValueError, KeyError, OSError) as exc:
        OUTPUT.unlink(missing_ok=True)
        print("SKIP:", exc)
