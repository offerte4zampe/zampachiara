import datetime as dt
import gzip
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from automation import build_weekly_newsletter as newsletter

NOW = dt.datetime(2026, 10, 28, 10, tzinfo=dt.timezone.utc)

class NewsletterBuilderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.catalog = Path(self.temp.name) / "catalog.json.gz"
        self.output = Path(self.temp.name) / "newsletter.json"
        self.patches = [
            patch.object(newsletter, "CATALOG", self.catalog),
            patch.object(newsletter, "OUTPUT", self.output)
        ]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)

    def write(self, offers, hours=1):
        stamp = (NOW - dt.timedelta(hours=hours)).isoformat()
        self.catalog.write_bytes(gzip.compress(json.dumps({
            "generated_at": stamp,
            "offers": [{**o, "checked_at": o.get("checked_at", stamp)} for o in offers]
        }).encode()))

    def offer(self, n):
        return {
            "title": f"Prodotto {n}", "variant": "2 kg",
            "merchant": "Negozio", "url": f"https://example.org/item/{n}",
            "available": True, "price": 12 + n, "weight_kg": 2
        }

    def test_generates_three_fresh_offers(self):
        self.write([self.offer(i) for i in range(3)])
        result = newsletter.build(NOW)
        self.assertEqual(len(result["offers"]), 3)
        self.assertTrue(self.output.exists())

    def test_rejects_stale_catalog(self):
        self.write([self.offer(i) for i in range(3)], hours=24)
        with self.assertRaises(ValueError):
            newsletter.build(NOW)

    def test_rejects_insufficient_offers(self):
        self.write([self.offer(i) for i in range(2)])
        with self.assertRaises(ValueError):
            newsletter.build(NOW)

    def test_rejects_unavailable_offers(self):
        rows = [self.offer(i) for i in range(3)]
        rows[0]["available"] = False
        self.write(rows)
        with self.assertRaises(ValueError):
            newsletter.build(NOW)

if __name__ == "__main__":
    unittest.main()
