import io
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from automation.cache_product_images import cache, allowed_url
from automation.apply_images import apply

class ProductImageTests(unittest.TestCase):
    def test_unverified_permissions_never_download(self):
        def forbidden(*args):raise AssertionError('Network must not be used')
        with tempfile.TemporaryDirectory() as folder:
            result,report=cache([{'id':'x','merchant_id':'a','image':'https://images.test/a.png'}],{'a':{'allow_cache':True,'permission_status':'unverified'}},Path(folder),fetch=forbidden)
            self.assertEqual(result,{})
            self.assertEqual(report['unlicensed'],1)

    def test_licensed_image_becomes_400_square_webp(self):
        data=io.BytesIO();Image.new('RGBA',(200,100),'red').save(data,'PNG')
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            manifest,report=cache([{'id':'../a','merchant_id':'a','image':'https://images.test/a.png'}],{'a':{'allow_cache':True,'permission_status':'verified','evidence':'https://license.test/terms','hosts':['images.test']}},root,fetch=lambda *_:data.getvalue())
            path=root/manifest['https://images.test/a.png'].lstrip('/')
            self.assertEqual(report['cached'],1)
            self.assertTrue(path.is_relative_to(root))
            with Image.open(path) as im:self.assertEqual(im.size,(400,400));self.assertEqual(im.format,'WEBP')
        self.assertFalse(allowed_url('https://images.test.evil/a',['images.test']))
        self.assertFalse(allowed_url('http://images.test/a',['images.test']))

    def test_markup_has_dimensions_alt_and_idempotent_fallback(self):
        html='<html><head></head><body><img src="https://images.test/a" alt=""></body></html>'
        result=apply(html,{'https://images.test/a':'Cibo & cane'}, {})
        for text in ['width="400"','height="400"','alt="Cibo &amp; cane"','decoding="async"','loading="lazy"','image-fallback.js','rel="preconnect"']:self.assertIn(text,result)
        self.assertEqual(apply(result,{'https://images.test/a':'Cibo & cane'}, {}),result)
