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

    def test_linked_card_image_is_decorative_and_home_spotlight_has_priority(self):
        html='<html><head></head><body><article class="spotlight-product"><img src="https://images.test/a" alt="Cibo"><h3><a href="/prodotto/cibo">Cibo</a></h3></article></body></html>'
        out=apply(html,{'https://images.test/a':'Cibo'}, {})
        self.assertIn('alt=""',out)
        self.assertIn('fetchpriority="high"',out)
        self.assertNotIn('loading="lazy"',out)
        self.assertEqual(out,apply(out,{'https://images.test/a':'Cibo'}, {}))

    def test_shared_cdn_is_not_permission_and_feed_image_cannot_be_replaced(self):
        from automation.image_policy import eligible,feed_image
        rule={'allow_cache':True,'permission_status':'verified','evidence':'https://license.test','scope':'approved_feed_assets','campaign_id':16143,'feed_id':600171}
        offer={'id':'bauzaar:1','image':'https://cdn.shopify.com/original.webp','source_type':'official_feed','affiliate_url':'https://tc.tradetracker.net/?c=16143&a=518044','image_source':feed_image('https://cdn.shopify.com/original.webp',16143,600171)}
        self.assertTrue(eligible(offer,rule))
        for change in [{'image':'https://cdn.shopify.com/other.webp'},{'source_type':'scraped'},{'affiliate_url':'https://tc.tradetracker.net/?c=31221&a=518044'},{'image_source':{}}]:self.assertFalse(eligible(offer|change,rule))

    def test_repeated_source_is_stored_once_and_home_priority_survives_the_cap(self):
        data=io.BytesIO();Image.new('RGBA',(10,10),'blue').save(data,'PNG')
        rows=[{'id':str(i),'merchant_id':'a','image':'https://images.test/'+str(i)+'.png'} for i in range(3)]
        rows.append(rows[2]|{'id':'duplicate'})
        calls=[]
        def fetch(url,hosts):calls.append(url);return data.getvalue()
        rules={'a':{'allow_cache':True,'permission_status':'verified','evidence':'https://license.test/terms','hosts':['images.test']}}
        with tempfile.TemporaryDirectory() as folder:
            manifest,report=cache(rows,rules,Path(folder),fetch=fetch,limit=1,priority_ids=['2'])
            self.assertEqual(list(manifest),['https://images.test/2.png'])
            self.assertEqual(calls,['https://images.test/2.png'])
