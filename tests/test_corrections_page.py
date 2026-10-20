import unittest
from automation.build_corrections_page import render


class CorrectionTests(unittest.TestCase):
    def test_no_fabricated_reports_and_escaped_evidence(self):
        template = '<html><head><title>Metodo</title></head><body><main>Metodo</main></body></html>'
        entry = dict(date='2026-10-20', origin='Controllo interno', title='<script>fake</script>', detail='Peso verificato', evidence='https://github.com/example')
        out = render(template, [entry], {})
        self.assertNotIn('<script>fake</script>', out)
        self.assertIn('&lt;script&gt;', out)
        self.assertIn('non ancora disponibili', out)
        self.assertIn('non invia automaticamente', out)
