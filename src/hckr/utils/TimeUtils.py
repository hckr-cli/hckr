from datetime import datetime

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

from .MessageUtils import error, success


def current_time(timezone: str = "UTC") -> datetime:
    """Return current time in the given timezone."""
    try:
        tz = ZoneInfo(timezone)
    except Exception as e:  # pragma: no cover - error should be very rare
        error(f"Invalid timezone: {timezone}\n{e}")
        raise
    return datetime.now(tz)


def convert(dt_str: str, from_tz: str, to_tz: str) -> datetime:
    """Convert ``dt_str`` from ``from_tz`` timezone to ``to_tz`` timezone."""
    try:
        from_zone = ZoneInfo(from_tz)
        to_zone = ZoneInfo(to_tz)
    except Exception as e:  # pragma: no cover - user input error
        error(f"Invalid timezone provided\n{e}")
        raise
    dt = datetime.fromisoformat(dt_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=from_zone)
    else:
        dt = dt.astimezone(from_zone)
    return dt.astimezone(to_zone)
