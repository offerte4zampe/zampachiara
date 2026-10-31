"""Image rights attach to an approved feed asset, never to a shared CDN host."""
import re
from urllib.parse import urlsplit,parse_qs

def permitted(rule):
    return bool(rule.get('allow_cache') is True and rule.get('permission_status')=='verified' and str(rule.get('evidence','')).startswith('https://'))

def feed_image(image,campaign,feed):
    return {'type':'official_feed','network':'TradeTracker','campaign_id':campaign,'feed_id':feed,'url':image}

def eligible(offer,rule):
    if not permitted(rule):return False
    if rule.get('scope')!='approved_feed_assets':return True
    source=offer.get('image_source') or {}
    if offer.get('source_type')!='official_feed' or source!=feed_image(offer.get('image'),rule.get('campaign_id'),rule.get('feed_id')):return False
    try:
        link=urlsplit(offer.get('affiliate_url',''));query=parse_qs(link.query)
        return link.scheme=='https' and link.netloc=='tc.tradetracker.net' and query.get('c')==[str(rule['campaign_id'])] and query.get('a')==['518044']
    except (ValueError,KeyError):return False

def local_image(offer,rule):
    path=offer.get('image_local','')
    return path if eligible(offer,rule) and re.fullmatch(r'/img/p/[a-f0-9]{24}-400\.webp',path) else ''
