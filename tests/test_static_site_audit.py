import tempfile
import unittest
from pathlib import Path
from automation.audit_site import inspect


BASE='''<!doctype html><html lang="it"><head><meta name="viewport" content="width=device-width"><meta name="description" content="D"><meta name="robots" content="index,follow"><link rel="canonical" href="https://offerte4zampe.it/{slug}"><title>T</title></head><body><a class="skip" href="#main">Salta</a><main id="main"><h1>H</h1>{body}</main></body></html>'''


class StaticSiteAuditTests(unittest.TestCase):
    def run_site(self,pages):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name,html in pages.items():(root/name).write_text(html)
            return inspect(root)

    def test_valid_page_and_commercial_link_require_sponsored(self):
        html=BASE.format(slug='one',body='<a href="https://tc.tradetracker.net/x" rel="sponsored noopener noreferrer" target="_blank">Shop</a><img src="x" alt="" width="4" height="5"><script type="application/ld+json">{"@context":"https://schema.org"}</script>')
        self.assertEqual(self.run_site({'one.html':html})['issues'],[])
        broken=html.replace('sponsored ','').replace(' width="4"','').replace('{"@context":"https://schema.org"}','{')
        rules={x['rule'] for x in self.run_site({'one.html':broken})['issues']}
        self.assertEqual(rules,{'commercial_rel_sponsored','image_dimensions','valid_json_ld'})

    def test_duplicate_and_noncanonical_urls_are_rejected_only_for_indexable_pages(self):
        one=BASE.format(slug='same',body='')
        two=BASE.format(slug='same',body='')
        rules={x['rule'] for x in self.run_site({'one.html':one,'two.html':two})['issues']}
        self.assertIn('unique_canonical',rules)
        noindex=two.replace('index,follow','noindex,follow').replace('<link rel="canonical" href="https://offerte4zampe.it/same">','')
        self.assertEqual(self.run_site({'one.html':one,'two.html':noindex})['issues'],[])

    def test_landmarks_metadata_images_and_safe_new_tabs_are_gated(self):
        html=BASE.format(slug='bad?x=1',body='<a target="_blank" href="https://example.com">X</a><img src="x">')
        html=html.replace(' lang="it"','').replace('<h1>H</h1>','').replace('class="skip"','class="other"')
        rules={x['rule'] for x in self.run_site({'bad.html':html})['issues']}
        self.assertTrue({'html_lang_it','one_h1','skip_link','image_alt','image_dimensions','safe_new_tab','clean_internal_canonical'}<=rules)

    def test_search_console_verification_token_is_not_a_content_page(self):
        token='google-site-verification: google123.html'
        result=self.run_site({'google123.html':token,'one.html':BASE.format(slug='one',body='')})
        self.assertEqual(result['pages_scanned'],1)
        self.assertEqual(result['issues'],[])
