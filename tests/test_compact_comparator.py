import unittest
from pathlib import Path
from automation.apply_compact_comparator import comparator,budget
class CompactComparatorTests(unittest.TestCase):
    def test_manual_tool_is_in_budget_and_transform_is_idempotent(self):
        root=Path(__file__).resolve().parents[1]
        html=(root/'site/confronta-cibo.html').read_text()
        out=comparator(html)
        self.assertNotIn('id="manual-tool"',out)
        self.assertIn('id="catalog-extra-filters"',out)
        self.assertIn('/calcolatore#manual-tool',out)
        self.assertEqual(out,comparator(out))
        manual=(root/'automation/partials/manual-food.html').read_text()
        result=budget('<main></main><body></body>',manual)
        self.assertIn('id="ap"',result);self.assertIn('id="bp"',result)
        self.assertEqual(result,budget(result,manual))
