import hashlib
import unittest
from automation.build_product_metadata import build
class ProductMetadataTests(unittest.TestCase):
    def test_names_only_and_deterministic_partition(self):
        offer = dict(id='shop:è', title='Nome & formato', price=10, affiliate_url='private')
        shards=build({'offers':[offer]})
        self.assertEqual(len(shards),256)
        key=hashlib.sha256(offer['id'].encode()).hexdigest()[:2]
        self.assertEqual(shards[key],{'shop:è':'Nome & formato'})
        self.assertEqual(sum(map(len,shards.values())),1)
    def test_invalid_and_ambiguous_ids_excluded(self):
        shards=build({'offers':[{'id':'x','title':'Uno'},{'id':'x','title':'Due'},{'id':'ok','title':' A '},{'id':None,'title':'a'},{'id':'bad','title':''}]})
        self.assertEqual({k:v for s in shards.values() for k,v in s.items()},{'ok':'A'})
