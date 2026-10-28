import json
import tempfile
import unittest
from pathlib import Path
from automation.improve_discovery import destination, enrich, inventory, build


def page(slug, body='', robots='index,follow'):
    return f'<html><head><meta name="robots" content="{robots}"><link rel="canonical" href="https://offerte4zampe.it/{slug}"></head><body>{body}</body></html>'


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.pages = {'/index.html': {'canonical':'/', 'indexable':True}, '/guide-risparmio.html': {'canonical':'/guide-risparmio','indexable':True}, '/confronta-cibo.html': {'canonical':'/confronta-cibo','indexable':True}}

    def test_only_existing_local_destinations_and_query_fragment_preserved(self):
        self.assertEqual(destination('confronta-cibo.html?q=A%26B&amp;shop=Shop#manual-tool', self.pages), '/confronta-cibo?q=A%26B&shop=Shop#manual-tool')
        self.assertEqual(destination('index.html', self.pages), '/')
        for url in ['https://shop.test/index.html?affiliate=abc','https://offerte4zampe.it.evil.test/index.html','unknown.html','prodotto.html?id=a%3A1','mailto:a@example.test','#main']:
            self.assertEqual(destination(url, self.pages), url)

    def test_menu_correct_destination_and_external_tracking_untouched(self):
        source = '<nav id="navlinks"><a href="scelte.html">Guide</a></nav><a href="https://shop.test/index.html?c=1&amp;a=2" rel="sponsored">Negozio</a><p>10,50 €</p>'
        result = enrich(source,self.pages)
        self.assertIn('href="/guide-risparmio">Guide</a>',result)
        self.assertIn('href="https://shop.test/index.html?c=1&amp;a=2" rel="sponsored"',result)
        self.assertIn('<p>10,50 €</p>',result)
        self.assertEqual(enrich(result,self.pages),result)

    def test_static_home_links_reduce_depth_and_never_promote_retired_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            site=Path(tmp)
            home='<nav id="navlinks"><a href="guide-risparmio.html">Guide</a></nav><div class="brand-links" id="home-brands"><a href="confronta-cibo.html?brand=Royal+Canin">Royal Canin</a></div><section class="section alt"><div class="wrap"><div class="section-heading"><div><span class="kicker">Acquisti più consapevoli</span><h2>Oltre il prezzo sul sacco.</h2></div></div></div></section><footer><ul></ul></footer>'
            (site/'index.html').write_text(page('',home))
            (site/'guide-risparmio.html').write_text(page('guide-risparmio','<a href="confrontare-prezzi-lettiere.html">Lettiere</a>'))
            (site/'confrontare-prezzi-lettiere.html').write_text(page('confrontare-prezzi-lettiere'))
            (site/'marca-royal-canin.html').write_text(page('marca-royal-canin'))
            (site/'marca-monge.html').write_text(page('marca-monge',robots='noindex,follow'))
            build(site)
            html=(site/'index.html').read_text()
            self.assertIn('href="/confrontare-prezzi-lettiere"',html)
            self.assertIn('href="/marca-royal-canin">Royal Canin',html)
            self.assertNotIn('/marca-monge',html)
            self.assertEqual(html.count('id="home-guides"'),1)
            report=json.loads((site/'data/discovery.json').read_text())
            self.assertEqual(report['after']['unreachable'],[])
            self.assertEqual(report['after']['max_link_depth'],1)
            self.assertGreater(report['before']['max_link_depth'],report['after']['max_link_depth'])
            build(site)
            self.assertEqual((site/'index.html').read_text(),html)
            self.assertIn('noindex,follow',(site/'marca-monge.html').read_text())

    def test_popular_searches_use_only_available_precise_brand_pages(self):
        pages = self.pages | {'/marca-royal-canin.html': {'canonical': '/marca-royal-canin', 'indexable': True}, '/marca-purina-pro-plan.html': {'canonical': '/marca-purina-pro-plan', 'indexable': True}}
        source = '<div class="popular-searches"><a href="/confronta-cibo?q=Royal%20Canin">Royal Canin</a><a href="/confronta-cibo?q=Purina">Purina</a><a href="/confronta-cibo?q=Trainer">Trainer</a></div>'
        result = enrich(source, pages, home=True)
        self.assertIn('href="/marca-royal-canin">Royal Canin</a>', result)
        self.assertIn('href="/marca-purina-pro-plan">Purina Pro Plan</a>', result)
        self.assertIn('href="/confronta-cibo?q=Trainer">Trainer</a>', result)
        self.assertEqual(enrich(result, pages, home=True), result)

    def test_repeated_catalog_navigation_does_not_duplicate_favorites(self):
        from automation.apply_navigation import apply
        html='<nav id="navlinks"><a href="/preferiti">Preferiti</a></nav>'
        self.assertEqual(apply(html).count('>Preferiti</a>'),1)


if __name__ == '__main__':
    unittest.main()
