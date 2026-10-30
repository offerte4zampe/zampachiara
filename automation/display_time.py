"""Italian display precision, with every timestamp interpreted in Europe/Rome."""
import datetime as dt
from zoneinfo import ZoneInfo


def format_timestamp(value):
    try:
        if len(value) == 10:
            return dt.date.fromisoformat(value).strftime('%d/%m/%Y')
        instant = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
        if instant.tzinfo is None:
            return value
        return instant.astimezone(ZoneInfo('Europe/Rome')).strftime('%d/%m/%Y, %H:%M')
    except (TypeError, ValueError, AttributeError):
        return 'non disponibile'
