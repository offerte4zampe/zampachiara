"""Freshness is based on observed offer timestamps, never failed fetch attempts."""
import datetime as dt
import json
import re
from html import escape


def stamp(value):
    try:
        result = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
        return result if result.tzinfo else None
    except (ValueError, TypeError, AttributeError):
        return None


def age_hours(value, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    checked = stamp(value)
    if checked is None or checked > now + dt.timedelta(minutes=5):
        return None
    return max(0, (now - checked).total_seconds() / 3600)


def source_freshness(source, offers, now=None):
    now = now or dt.datetime.now(dt.timezone.utc)
    times = [stamp(o.get('checked_at')) for o in offers if o.get('merchant_id') == source['id']]
    times = [t for t in times if t and t <= now + dt.timedelta(minutes=5)]
    latest = max(times).isoformat() if times else None
    age = age_hours(latest, now)
    return {**source, 'attempted_at': source.get('attempted_at', source.get('checked_at')),
            'checked_at': latest, 'latest_offer_checked_at': latest,
            'data_age_hours': round(age, 2) if age is not None else None,
            'freshness': 'unknown' if age is None else 'stale' if age > 12 else 'fresh'}


def label(value, now=None):
    age = age_hours(value, now)
    return 'Data aggiornamento non disponibile' if age is None else f'Dati non aggiornati da {int(age)} ore' if age > 12 else ''


def banner(html, sources, now=None):
    messages = [escape(s['name']) + ': ' + label(s.get('checked_at'), now)
                for s in sources if label(s.get('checked_at'), now)]
    data = json.dumps([{'name': s['name'], 'checked_at': s.get('checked_at')} for s in sources], ensure_ascii=False).replace('<', '\\u003c')
    content = '<!-- freshness:start--><div id="catalog-freshness" class="notice" role="status"' + ('' if messages else ' hidden') + '>'
    content += ''.join('<p>' + m + '</p>' for m in messages) + '</div><script type="application/json" id="catalog-freshness-data">' + data + '</script><!-- freshness:end-->'
    if '<!-- freshness:start-->' in html:
        return re.sub(r'<!-- freshness:start-->.*?<!-- freshness:end-->', lambda _: content, html, flags=re.S)
    return html.replace('<div id="catalog-filters"', content + '<div id="catalog-filters"', 1)
