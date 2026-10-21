import unittest
from automation.remove_unverified_ads import apply


class AdLoaderTests(unittest.TestCase):
    def test_remove_loader_preserve_ownership_content_and_affiliation(self):
        html = '<meta name="google-adsense-account" content="ca-pub-1"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1" crossorigin="anonymous"></script><a href="https://tc.tradetracker.net/?c=16143" rel="sponsored">Bauzaar</a>'
        result = apply(html)
        self.assertNotIn('<script', result)
        self.assertIn('google-adsense-account', result)
        self.assertIn('tc.tradetracker.net', result)
        self.assertEqual(apply(result), result)

    def test_case_quotes_and_unrelated_scripts(self):
        html = "<SCRIPT ASYNC SRC='//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js'></SCRIPT>"
        self.assertEqual(apply(html), '')
        for script in ['<script src="assets/catalog.js" defer></script>', '<script type="application/ld+json">{"@type":"Product"}</script>', '<script src="https://example.test/adsbygoogle.js"></script>']:
            self.assertEqual(apply(script), script)
