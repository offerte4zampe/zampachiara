"""Apply small display fixes to generated HTML without changing machine data."""
import re
from pathlib import Path
try:
    from .display_time import format_timestamp
except ImportError:
    from display_time import format_timestamp
ROOT = Path(__file__).resolve().parents[1]
ISO = r'\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})\b'
UTC = r'\b(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) UTC\b'


def apply(html):
    # Script JSON, attributes and style contents retain their machine formats.
    tokens = re.split(r'(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<[^>]+>)', html, flags=re.S | re.I)
    for i, token in enumerate(tokens):
        if token.startswith('<'):
            continue
        token = re.sub(ISO, lambda m: format_timestamp(m[0]), token)
        token = re.sub(UTC, lambda m: format_timestamp(m[1] + 'T' + m[2] + ':00Z'), token)
        token = re.sub(r'\b\d{4}-\d{2}-\d{2}\b', lambda m: format_timestamp(m[0]), token)
        tokens[i] = token.replace('1 ore fa', '1 ora fa')
    html = ''.join(tokens).replace('* Totale stimato crescente', 'Totale stimato crescente')
    html = html.replace('al prezzo da cercare.', 'al prezzo giusto.')
    html = re.sub(r'<label>(<input\b[^>]*\bid="catalog-sale"[^>]*>.*?</label>)', r'<label hidden style="display:none">\1', html, flags=re.S)
    return html


def main():
    changed = 0
    for p in (ROOT / 'site').rglob('*.html'):
        before = p.read_text()
        after = apply(before)
        if after != before:
            p.write_text(after)
            changed += 1
    print('Display micro-fixes applied:', changed)


if __name__ == '__main__':
    main()
