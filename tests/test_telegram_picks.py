import datetime
import unittest

from automation.build_home_data import telegram_picks


class TelegramPicksTests(unittest.TestCase):
    def test_only_fresh_partner_photos_with_verified_price_and_pack(self):
        now = datetime.datetime(2026, 10, 31, 8, 0, tzinfo=datetime.timezone.utc)
        stamp = '2026-10-31T07:00:00+00:00'
        source = {'id': 'isola-dei-tesori', 'status': 'ok', 'checked_at': stamp}
        base = dict(
            id='isola-dei-tesori:1', merchant_id='isola-dei-tesori',
            merchant='Isola dei Tesori', brand='Royal Canin',
            title='Royal Canin Dog Medium Adult 15 kg', category='crocchette cane',
            variant='', canonical_format='15 kg', price=74.39, weight_kg=15,
            available=True, checked_at=stamp,
            image='https://www.isoladeitesori.it/images/royal-canin-15kg.jpg',
            product_url='/prodotto/royal-canin-dog-medium-adult-15-kg',
        )
        invalid = [
            base | {'id': 'evil', 'image': 'https://evil.example/royal.jpg'},
            base | {'id': 'webp', 'image': 'https://www.isoladeitesori.it/images/royal.webp'},
            base | {'id': 'stale', 'checked_at': '2026-10-29T07:00:00+00:00'},
            base | {'id': 'unavailable', 'available': False},
            base | {'id': 'free', 'price': 0},
            base | {'id': 'medicated', 'title': 'Dieta veterinaria renal per cane 15 kg'},
        ]
        catalog = dict(
            generated_at=stamp,
            sources=[source, {'id': 'webpet', 'status': 'ok', 'checked_at': stamp}],
            offers=[base, *invalid],
        )
        result = telegram_picks(catalog, now)
        self.assertEqual([o['id'] for o in result['offers']], ['isola-dei-tesori:1'])
        self.assertEqual(result['offers'][0]['price'], 74.39)
        self.assertEqual(result['offers'][0]['product_url'], base['product_url'])
        self.assertNotIn('affiliate_url', result['offers'][0])
        self.assertEqual([s['id'] for s in result['sources']], ['isola-dei-tesori'])

    def test_unhealthy_partner_source_yields_no_candidates(self):
        now = datetime.datetime(2026, 10, 31, 8, 0, tzinfo=datetime.timezone.utc)
        stamp = '2026-10-31T07:00:00+00:00'
        offer = dict(id='paco:1', merchant_id='paco', merchant='Paco Pet Shop',
                     brand='Almo Nature', title='Almo Nature umido per gatti 55 g',
                     category='umido gatti', variant='55 g', price=1.5, weight_kg=.055,
                     available=True, checked_at=stamp,
                     image='https://www.pacopetshop.it/img/food.jpg')
        catalog = dict(generated_at=stamp, sources=[dict(id='paco', status='error', checked_at=stamp)], offers=[offer])
        self.assertEqual(telegram_picks(catalog, now)['offers'], [])
