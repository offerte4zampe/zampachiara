import datetime as dt
import json
import re
import unittest
from automation.build_savings_guides import food_examples, food_content, litter_examples, document, pack_content, shipping_content, observed_examples, history_content, identity_examples, identity_content


class SavingsGuidesTests(unittest.TestCase):
    def setUp(self):
        self.now=dt.datetime.now(dt.timezone.utc)
        # Synthetic fixtures used only in tests, never written as public offers.
        self.o=dict(id='a',merchant_id='a',merchant='Shop A',brand='Brand',title='Food cane',category='Crocchette cani',price=12,weight_kg=2,available=True,url='https://example.com/product',checked_at=self.now.isoformat(),gtin='4006381333931')

    def test_manual_ration_is_explicit_and_price_math_uses_actual_net_weight(self):
        html=food_content([self.o],self.now)
        self.assertIn('6,00 €/kg',html);self.assertIn('1,50 €',html);self.assertIn('45,00 €',html)
        self.assertIn('Non è una razione consigliata',html);self.assertIn('spedizione esclusa',html)
        self.assertIn(self.o['url'],html)

    def test_stale_missing_weight_medical_and_unavailable_examples_are_not_used(self):
        for patch in [dict(checked_at='2020-01-01T00:00:00Z'),dict(weight_kg=None),dict(weight_kg=float('nan')),dict(title='Dieta veterinaria cane'),dict(available=False),dict(price=-3)]:
            self.assertEqual(food_examples([self.o|patch],self.now),[])
        html=food_content([],self.now);self.assertNotIn('<tr>',html)

    def test_litter_comparison_requires_exact_code_brand_and_net_quantity(self):
        a=self.o|dict(title='Lettiera 2 kg',category='Lettiera');b=a|dict(id='b',merchant_id='b',merchant='Shop B')
        self.assertEqual(len(litter_examples([a,b],self.now)),1)
        for patch in [dict(weight_kg=3),dict(gtin=''),dict(brand='Other'),dict(weight_kg=None)]:
            self.assertEqual(litter_examples([a,b|patch],self.now),[])

    def test_article_metadata_and_visible_breadcrumb_correspond(self):
        html=document('<html><head><title>Method</title></head><body><main></main></body></html>','sample','Title','Description','<h2>Content</h2>',self.now)
        data=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html)[1])
        article=data['@graph'][0];self.assertEqual(article['headline'],'Title')
        self.assertNotIn('datePublished',article);self.assertEqual(article['author']['@type'],'Organization')
        self.assertIn('guide-risparmio.html',html)

    def test_pack_comparison_keeps_tracking_and_does_not_fill_unknown_weight(self):
        offer=self.o|dict(affiliate_url='https://example.com/tracked')
        html=pack_content([offer],self.now)
        self.assertIn('6,00 €/kg',html)
        self.assertIn('https://example.com/tracked',html)
        self.assertIn('sponsored',html)
        self.assertIn('ricette differenti',html)
        self.assertNotIn('<table',pack_content([offer|dict(weight_kg=None)],self.now))

    def test_shipping_rules_expire_and_preserve_uncertainty_without_free_defaults(self):
        rules={'checked_at':self.now.date().isoformat(),'merchants':{'a':{'name':'A','note':'Tariffa da verificare, soglia ambigua','source':'https://example.com/shipping'}}}
        html=shipping_content([],self.now,rules)
        self.assertIn('Tariffa da verificare, soglia ambigua',html)
        self.assertIn('https://example.com/shipping',html)
        for day in ['2020-01-01',(self.now.date()+dt.timedelta(days=1)).isoformat(),'not-a-date']:
            self.assertNotIn('<table',shipping_content([],self.now,rules|{'checked_at':day}))

    def test_history_counts_real_days_and_rejects_changed_identity_and_bad_rows(self):
        import hashlib
        fingerprint=hashlib.sha256(json.dumps([self.o.get(k) for k in ('merchant_id','title','variant','brand','gtin','weight_kg')],ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
        day=self.now.date().isoformat()
        record={'day':day,'low':10,'last':12,'high':14}
        history={'identities':{'a':fingerprint},'offers':{'a':[record,record|{'low':9},{'day':'2099-01-01','low':1,'last':1,'high':1},record|{'low':-4},record|{'high':8}]}}
        example=observed_examples([self.o],self.now,history)[0][1]
        self.assertEqual(example['days'],1)
        self.assertEqual(example['low'],9)
        self.assertEqual(example['high'],14)
        self.assertEqual(observed_examples([self.o|{'variant':'New recipe'}],self.now,history),[])
        self.assertNotIn('<table',history_content([self.o],self.now,{}))
        html=history_content([self.o],self.now,history)
        self.assertIn('9,00 €',html)
        self.assertIn(day,html)

    def test_identity_guide_requires_exact_format_and_preserves_merchant_tracking(self):
        other=self.o|dict(id='b',merchant_id='b',merchant='Shop B',affiliate_url='https://example.com/tracked')
        self.assertEqual(len(identity_examples([self.o,other],self.now)),1)
        html=identity_content([self.o,other],self.now)
        self.assertIn('4006381333931',html)
        self.assertIn('https://example.com/tracked',html)
        self.assertIn('sponsored',html)
        self.assertIn('spedizione esclusa',html)
        for patch in [dict(gtin='4006381333932'),dict(weight_kg=3),dict(brand='Other'),dict(available=False),dict(checked_at='2020-01-01T00:00:00Z')]:
            self.assertEqual(identity_examples([self.o,other|patch],self.now),[])
            self.assertNotIn('<table',identity_content([self.o,other|patch],self.now))
