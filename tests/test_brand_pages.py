import datetime
import unittest
from automation.build_brand_pages import select


class BrandPagesTests(unittest.TestCase):
    def test_exact_brand_freshness_and_source_rotation(self):
        now=datetime.datetime.now(datetime.timezone.utc).isoformat()
        base=dict(id='1',title='Food',brand='Monge',merchant='A',price=10,available=True,url='https://example.com/food',checked_at=now)
        rows,picked=select([base,base|dict(id='2',title='Other',merchant='B'),base|dict(id='3',brand='Monge VetSolution'),base|dict(id='4',checked_at='2020-01-01T00:00:00+00:00'),base|dict(id='5',available=False)],'Monge')
        self.assertEqual(len(rows),3)
        self.assertEqual([o['merchant'] for o in picked],['A','B','A'])
