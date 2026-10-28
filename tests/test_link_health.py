import datetime as dt
import unittest
from automation.check_merchant_links import safe_product, record, blocked, candidates, apply, NoRedirect


class LinkHealthTests(unittest.TestCase):
    def setUp(self):
        self.now = dt.datetime(2026,10,20,12,tzinfo=dt.timezone.utc)
        self.offer = dict(id='webpet:1',merchant_id='webpet',merchant='WebPet',url='https://www.webpet.it/products/food?variant=1',affiliate_url='https://tc.tradetracker.net/?c=999')

    def test_only_direct_exact_allowlisted_product_urls(self):
        self.assertTrue(safe_product(self.offer))
        for url in ['https://tc.tradetracker.net/?c=999','https://www.webpet.it/cart','https://www.webpet.it/products/food?variant=1&utm_source=x','https://www.webpet.it.evil.test/products/food?variant=1','https://user@www.webpet.it/products/food?variant=1','http://www.webpet.it/products/food?variant=1']:
            self.assertFalse(safe_product(dict(self.offer,url=url)))
        self.assertIsNone(NoRedirect().redirect_request(None,None,302,'',{},'https://tc.tradetracker.net/'))

    def test_two_separate_failures_same_url_required_and_expire(self):
        one=record({},self.offer,404,self.now)
        self.assertFalse(blocked(one,self.offer,self.now))
        soon=record(one,self.offer,404,self.now+dt.timedelta(hours=1))
        self.assertFalse(blocked(soon,self.offer,self.now+dt.timedelta(hours=1)))
        later=self.now+dt.timedelta(hours=6)
        two=record(one,self.offer,410,later)
        self.assertTrue(blocked(two,self.offer,later))
        self.assertFalse(blocked(two,dict(self.offer,url=self.offer['url']+'2'),later))
        self.assertFalse(blocked(two,self.offer,later+dt.timedelta(days=8)))
        self.assertFalse(blocked(two,self.offer,self.now))

    def test_recovery_and_unknown_results_never_suppress(self):
        old=record(record({},self.offer,404,self.now-dt.timedelta(hours=7)),self.offer,404,self.now)
        for code in [200,301,403,405,429,500,'network_error','robots_unverified_or_disallowed']:
            entry=record(old,self.offer,code,self.now+dt.timedelta(hours=6))
            self.assertFalse(blocked(entry,self.offer,self.now+dt.timedelta(hours=6)))

    def test_round_robin_rotation_and_pending_confirmation(self):
        a=self.offer;b=dict(a,id='bauzaar:2',merchant_id='bauzaar',url='https://www.bauzaar.it/products/food?variant=2')
        c=dict(a,id='webpet:3',url='https://www.webpet.it/products/other?variant=3')
        cache={a['id']:record({},a,404,self.now-dt.timedelta(hours=7))}
        picked=candidates([c,a,b],cache,self.now,2)
        self.assertEqual({o['merchant_id'] for o in picked},{'webpet','bauzaar'})
        self.assertEqual(picked[1]['id'],a['id'])
        cache[a['id']]=record({},a,200,self.now)
        self.assertNotIn(a,candidates([c,a,b],cache,self.now,10))

    def test_budget_and_report_do_not_change_prices_or_follow_affiliate_urls(self):
        called=[]
        def head(o): called.append(o['url']);return 200
        catalog=dict(offers=[dict(self.offer,price=12),dict(self.offer,id='webpet:2',url='https://www.webpet.it/products/second?variant=2',price=23)])
        output,cache,report=apply(catalog,{},self.now,head,limit=1,pause=0)
        self.assertEqual(output,catalog);self.assertEqual(len(called),1)
        self.assertEqual(report['attempted_this_run'],1);self.assertEqual(report['suppressed'],[])
        self.assertTrue(all('tradetracker' not in u for u in called))
        self.assertEqual(len(cache),1)

    def test_confirmed_dead_url_hidden_without_rechecking_or_mutating_source(self):
        entry=record(record({},self.offer,404,self.now-dt.timedelta(hours=7)),self.offer,404,self.now)
        def forbidden(o): raise AssertionError('Unnecessary network request')
        catalog=dict(offers=[dict(self.offer,price=12)])
        output,_,report=apply(catalog,{self.offer['id']:entry},self.now,forbidden,pause=0)
        self.assertEqual(output['offers'],[]);self.assertEqual(catalog['offers'][0]['price'],12)
        self.assertEqual(report['suppressed'][0]['id'],self.offer['id'])

    def test_all_five_stores_are_checked_without_affiliate_redirects(self):
        offers=[dict(id=s+':1',merchant_id=s,url=u) for s,u in [
            ('bauzaar','https://www.bauzaar.it/products/food?variant=1'),
            ('webpet','https://www.webpet.it/products/food?variant=1'),
            ('animaliapet','https://www.animaliapet.eu/products/food?variant=1'),
            ('isola-dei-tesori','https://www.isoladeitesori.it/prodotto/food/0001.html'),
            ('paco','https://www.pacopetshop.it/it/brand/1-food.htm')]]
        self.assertTrue(all(safe_product(o) for o in offers))
        self.assertEqual(len(candidates(offers,{},self.now,5)),5)
        for url in ['https://www.pacopetshop.it/directlinking/?tt=1','https://www.pacopetshop.it/it/brand/1-food.htm?x=1']:
            self.assertFalse(safe_product(dict(offers[-1],url=url)))
