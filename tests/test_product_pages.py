import importlib.util, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('products',Path(__file__).resolve().parents[1]/'automation/build_product_pages.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
class ProductIdentity(unittest.TestCase):
 def test_different_recipe_or_shop_never_merged(self):
  a=dict(merchant='A',title='Adult pollo',brand='B')
  self.assertFalse(mod.same_product(a,dict(a,title='Adult salmone')))
  self.assertFalse(mod.same_product(a,dict(a,merchant='C')))
  self.assertTrue(mod.same_product(a,dict(a,variant='12 kg')))

class Freshness(unittest.TestCase):
 def test_stale_or_missing_dates_not_current(self):
  import datetime as dt
  now=dt.datetime(2026,10,19,tzinfo=dt.timezone.utc)
  self.assertTrue(mod.fresh({'checked_at':'2026-10-18T12:00:00+00:00'},now))
  for value in ['2026-10-01T00:00:00+00:00','2026-10-20T00:00:00+00:00','invalid','2026-10-18']:
   self.assertFalse(mod.fresh({'checked_at':value},now))
 def test_removed_seed_does_not_retain_old_available_price(self):
  import tempfile,gzip,json
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);(root/'site/data').mkdir(parents=True)
   template='<html><head><title>Old</title><meta name="robots" content="index,follow"></head><main>old</main></html>'
   (root/'site/chi-siamo.html').write_text(template);(root/'site/monge-adult-cat-pollo.html').write_text('<h1>Monge pollo</h1><p>Disponibile 12 €</p>')
   (root/'site/sitemap.xml').write_text('<urlset><url><loc>https://offerte4zampe.it/monge-adult-cat-pollo</loc></url></urlset>')
   (root/'site/data/catalog.json.gz').write_bytes(gzip.compress(json.dumps({'offers':[],'generated_at':'2026-10-19'}).encode()))
   old=mod.ROOT
   try:mod.ROOT=root;mod.build()
   finally:mod.ROOT=old
   content=(root/'site/monge-adult-cat-pollo.html').read_text()
   self.assertNotIn('12 €',content);self.assertIn('noindex,follow',content)
   self.assertNotIn('monge-adult-cat-pollo',(root/'site/sitemap.xml').read_text())
