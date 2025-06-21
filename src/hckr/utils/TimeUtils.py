from datetime import datetime
from zoneinfo import ZoneInfo, available_timezones
from .MessageUtils import error


def suggest_timezones(query: str) -> str:
    """Return a comma separated list of matching timezones."""
    try:
        matches = [tz for tz in available_timezones() if query.lower() in tz.lower()]
        if not matches:
            return ""
        return ", ".join(sorted(matches)[:5])
    except Exception:
        return ""


def display(dt_input: str | None, fmt: str, timezone: str | None) -> str:
    """Format the given datetime string in the requested timezone and format."""
    tz = None
    if timezone:
        try:
            tz = ZoneInfo(timezone)
        except Exception as e:
            hint = suggest_timezones(timezone)
            msg = f"Invalid timezone: {timezone}\n{e}"
            if hint:
                msg += f"\nDid you mean: {hint}?"
            msg += ("\nSee https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
                    " for a list of valid timezones.")
            error(msg)
            raise
    if not tz:
        tz = datetime.now().astimezone().tzinfo

    if dt_input:
        try:
            dt = datetime.fromisoformat(dt_input)
        except Exception as e:
            error(
                "Invalid datetime string. Expected ISO format YYYY-MM-DD HH:MM:SS"
                f"\n{e}\nRefer to https://docs.python.org/3/library/datetime.html"
                "#datetime.datetime.fromisoformat" )
            raise
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=tz)
        else:
            dt = dt.astimezone(tz)
    else:
        dt = datetime.now(tz)

    try:
        return dt.strftime(fmt)
    except Exception as e:
        error(
            f"Invalid datetime format: {fmt}\n{e}\nSee https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes"
        )
        raise
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
