#!/usr/bin/env python3
"""Refresh links to recent headlines; do NOT copy article bodies or assert editorial verification."""
import json, re, sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

DEST = Path(__file__).resolve().parents[1] / "site" / "data" / "news.json"
QUERY = "animali domestici OR cani OR gatti veterinari when:7d"
FEED = "https://news.google.com/rss/search?q=" + quote(QUERY) + "&hl=it&gl=IT&ceid=IT:it"

def clean(text):
    return re.sub(r"\s+", " ", (text or "")).strip()[:180]

def parse(xml, now=None):
    now = now or datetime.now(timezone.utc)
    root = ET.fromstring(xml)
    items, seen = [], set()
    for node in root.findall(".//channel/item"):
        title = clean(node.findtext("title"))
        link = (node.findtext("link") or "").strip()
        u = urlparse(link)
        date_text = node.findtext("pubDate") or ""
        if len(title) < 18 or u.scheme != "https" or u.hostname != "news.google.com" or link in seen:
            continue
        try:
            dt = parsedate_to_datetime(date_text).astimezone(timezone.utc)
            if not (now - timedelta(days=8) <= dt <= now + timedelta(hours=6)):
                continue
        except (ValueError, TypeError, OverflowError):
            continue
        seen.add(link)
        items.append({
            "title": title,
            "url": link,
            "source": clean(node.findtext("source")) or "Google News",
            "date": dt.strftime("%d/%m/%Y"),
            "category": "Feed RSS · non verificato editorialmente",
            "verified": False,
            "_time": dt.isoformat(),
        })
    items.sort(key=lambda x:x["_time"], reverse=True)
    for item in items: item.pop("_time", None)
    return items[:9]

def main():
    req=Request(FEED,headers={"User-Agent":"Offerte4ZampeNewsLinkReader/1.0"})
    try:
        with urlopen(req,timeout=20) as response: rss=response.read(400000)
        items=parse(rss)
    except Exception as exc:
        print("News feed unavailable; existing data retained:",exc,file=sys.stderr)
        return 0
    if len(items)<3:
        print("Too few recent items; existing data retained")
        return 0
    old = json.loads(DEST.read_text(encoding="utf-8"))
    manual = [item for item in old.get("items",[]) if item.get("verified") is True]
    urls={item.get("url") for item in manual}
    combined=manual[:3]+[item for item in items if item["url"] not in urls][:9-len(manual[:3])]
    updated={"updated_at":datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")+" — i link RSS non sono verificati editorialmente","items":combined}
    DEST.write_text(json.dumps(updated,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Updated",len(combined),"news links")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
