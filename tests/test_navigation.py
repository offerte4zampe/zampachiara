import unittest
from automation.apply_navigation import apply


class NavigationTests(unittest.TestCase):
    def test_scoped_and_idempotent(self):
        old = '<a href="confronta-cibo.html?sale=1">Offerte</a>'
        cta = '<a class="navcta" href="confronta-cibo.html">Cerca prodotti ↗</a>'
        html = old + '<nav class="navlinks" id="navlinks" aria-label="Principale">' + old + cta + '<a href="guide-risparmio.html" aria-current="page">Guide</a></nav>' + '<a href="https://tc.tradetracker.net/?c=16143" rel="sponsored">Prodotto</a>'
        result = apply(html)
        self.assertTrue(result.startswith(old))
        self.assertIn('<a href="prodotti.html">Prodotti</a>', result)
        self.assertNotIn('Cerca prodotti', result)
        self.assertIn('aria-current="page">Guide', result)
        self.assertIn('https://tc.tradetracker.net/?c=16143', result)
        self.assertEqual(apply(result), result)

    def test_other_navigation_unchanged(self):
        html = '<nav id="categories"><a href="confronta-cibo.html?sale=1">Offerte</a></nav>'
        self.assertEqual(apply(html), html)
