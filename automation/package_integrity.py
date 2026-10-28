"""Resolve explicit selling quantities; contradictory feed weights stay unconfirmed."""
import re
try:
    from .update_catalog import weight
except ImportError:
    from update_catalog import weight


def pack_count(title):
    text=str(title or '').lower()
    m=re.search(r'\bconfezione\s+da\s+(\d+)\s*(?:pezzi|pz|lattine|buste|bustine)\b',text)
    return int(m[1]) if m and 0<int(m[1])<=1000 else 1


def reconcile(offer):
    if offer.get('quantity_verified') is False:
        return
    # A verified selected-variant label is stronger than the unit-pricing feed field.
    if offer.get('weight_source')=='merchant:selected_variant':
        return
    title_kg=weight(offer.get('title',''))
    variant_kg=weight(offer.get('variant',''))
    current=offer.get('weight_kg')
    if offer.get('merchant_id')=='bauzaar' and title_kg and variant_kg and abs(title_kg-variant_kg)>1e-6:
        offer.update(weight_kg=None,weight_source='',weight_conflict=True,
                     weight_evidence={'title_kg':title_kg,'feed_unit_pricing_kg':variant_kg})
        return
    if offer.get('weight_conflict'):
        return
    inferred=offer.get('weight_source') in ('explicit_package_label','official_feed:title')
    if not current or inferred:
        kg=variant_kg or title_kg
        offer.update(weight_kg=kg,weight_source='explicit_package_label' if kg else '')
