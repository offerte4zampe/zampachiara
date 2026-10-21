import datetime
import unittest
from automation.build_line_pages import select,render
class LinePagesTests(unittest.TestCase):
 def test_explicit_line_and_freshness_not_fuzzy_recipe(self):
  now=datetime.datetime.now(datetime.timezone.utc)
  base=dict(id='a',brand='Monge',title='Monge BWild Grain Free 2 kg',merchant='A',price=10,available=True,url='https://example.com/a',checked_at=now.isoformat(),weight_kg=2)
  bad=[base|dict(title='Monge Natural'),base|dict(brand='Other BWild'),base|dict(title='Monge BWildcard'),base|dict(available=False),base|dict(price=float('nan')),base|dict(checked_at='2020-01-01T00:00:00Z')]
  rows,picked=select([base,base|dict(id='b',merchant='B',title='Monge BWild Low Grain 4 kg')]+bad,now)
  self.assertEqual(len(rows),2);self.assertEqual([o['id'] for o in picked],['a','b'])
 def test_low_coverage_hides_prices_and_uses_noindex(self):
  template='<title>x</title><meta name="robots" content="index,follow"><link rel="canonical" href="https://offerte4zampe.it/chi-siamo"><main>x</main>'
  html=render(template,{'offers':[]})
  self.assertIn('noindex,follow',html);self.assertNotIn('catalog-price',html)

 def test_internal_exact_ids_and_html_escaping_on_publishable_selection(self):
  now=datetime.datetime.now(datetime.timezone.utc)
  offers=[dict(id=f'shop:{i}',brand='Monge BWild',title=f'Monge BWild <script> {i}',merchant='A' if i%2 else 'B',price=10,available=True,url='https://example.com/a',checked_at=now.isoformat(),variant='2 kg',weight_kg=2) for i in range(12)]
  template='<title>x</title><meta name="robots" content="index,follow"><link rel="canonical" href="https://offerte4zampe.it/chi-siamo"></head><main>x</main>'
  html=render(template,{'offers':offers},now)
  self.assertEqual(html.count('class="catalog-card"'),12)
  self.assertIn('prodotto.html?id=shop%3A0',html)
  self.assertNotIn('<script> 0',html)
  self.assertIn('https://offerte4zampe.it/linea-monge-bwild',html)
  self.assertIn('BreadcrumbList',html)
