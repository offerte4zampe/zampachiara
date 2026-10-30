"""Load the shared product display formatter before the legacy client resolver."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def apply(html):
    script='<script src="assets/product-metadata.js" defer></script>'
    if script not in html:
        html=html.replace('<script src="assets/product.js',script+'<script src="assets/product.js')
    return html
if __name__=='__main__':
    path=ROOT/'site/prodotto.html';path.write_text(apply(path.read_text()))
