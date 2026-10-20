import json
import re
import unittest
from automation.list_schema import append_list_schema


class ListSchemaTests(unittest.TestCase):
    def test_visible_labels_escape_and_idempotence_without_product_claims(self):
        source='<html><head></head><main><a href="https://example.com/a">Product</a></main></html>'
        values=[('Product </script>','https://example.com/a'),('Invalid','javascript:alert(1)')]
        html=append_list_schema(source,'List',values)
        self.assertEqual(html,append_list_schema(html,'List',values))
        data=json.loads(re.search(r'<script id="o4z-itemlist" type="application/ld\+json">(.*?)</script>',html)[1])
        self.assertEqual(len(data['itemListElement']),1)
        self.assertEqual(data['itemListElement'][0]['name'],'Product </script>')
        self.assertNotIn('aggregateRating',data)
        self.assertNotIn('offers',data)
