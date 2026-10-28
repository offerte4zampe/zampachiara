#!/usr/bin/env python3
"""Build weekly site article and social copy from the exact newsletter payload."""
import datetime as dt
import html
import json
import os
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "newsletter-approved.json"
SITE = ROOT / "site"
def build():
    p = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    day = dt.datetime.now(dt.timezone.utc).date().isoformat()
    if p.get("verified_on") != day or not 3 <= len(p.get("offers", [])) <= 5:
        raise ValueError("Newsletter selection missing, stale or incomplete")
    slug = "offerte-settimana-" + day
    path = SITE / "offerte" / (slug + ".html")
    path.parent.mkdir(parents=True, exist_ok=True)
    title = "5 prodotti per animali da confrontare" if len(p["offers"]) == 5 else "Prodotti per animali da confrontare"
    heading = f"{title} · {day}"
    items = []
    social = [f"🐾 Offerte da fiutare · {day}", "Ecco i prodotti selezionati questa settimana dal nostro comparatore:"]
    for o in p["offers"]:
        url = str(o["url"])
        parsed = urlsplit(url)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("Unsafe offer link")
        name = str(o["name"])
        price = str(o["price"])
        shop = str(o["shop"])
        fmt = str(o["format"])
        items.append(f'<li><strong>{html.escape(name)}</strong> ({html.escape(fmt)}) — {html.escape(price)} da {html.escape(shop)}. <a rel="nofollow sponsored noopener" href="{html.escape(url, quote=True)}">Controlla prezzo e disponibilità</a></li>')
        social.append(f"• {name} ({fmt}) — {price} · {shop}")
    article_url = f"https://offerte4zampe.it/offerte/{slug}.html"
    social.extend(["", "Prezzi rilevati dal catalogo: verifica sempre il prezzo finale e la spedizione presso il negozio.", f"🔎 Dettagli: {article_url}", "Alcuni collegamenti possono essere affiliati. #Offerte4Zampe #AnimaliDomestici"])
    page = f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(heading)} | Offerte a 4 Zampe</title><meta name="description" content="Cinque prodotti per animali selezionati dal catalogo, con prezzi e negozi da confrontare."><link rel="canonical" href="{article_url}"></head><body><main><p><a href="/">Offerte a 4 Zampe</a></p><h1>{html.escape(heading)}</h1><p>Una selezione basata sul prezzo per unità di peso, non una classifica di sconti. Rilevazioni del {day}: prezzi e disponibilità possono variare; spedizione esclusa salvo indicazione diversa.</p><ol>{''.join(items)}</ol><p>Prima di acquistare, confronta il prezzo totale e controlla formato, disponibilità e condizioni del negozio.</p><p>Trasparenza: alcuni collegamenti sono affiliati e possiamo ricevere una commissione senza costi aggiuntivi per te.</p><p><a href="/">Torna al comparatore</a></p></main></body></html>"""
    path.write_text(page, encoding="utf-8")
    out = ROOT / "automation" / "weekly-social-draft.json"
    out.write_text(json.dumps({"date":day,"article_url":article_url,"facebook": "\n".join(social), "instagram": "\n".join(social).replace(article_url,"Link all'articolo nel sito: offerte4zampe.it"),"status":"draft_not_published"},ensure_ascii=False,indent=2),encoding="utf-8")
    print("Built", path.relative_to(ROOT), "and social draft")
if __name__ == "__main__":
    build()
