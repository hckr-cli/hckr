from __future__ import annotations

from datetime import datetime

try:
    from zoneinfo import ZoneInfo, available_timezones
except ImportError:
    from backports.zoneinfo import ZoneInfo, available_timezones
from .MessageUtils import error, PError


# Mapping of common timezone abbreviations to IANA timezone names
TIMEZONE_ABBREVIATIONS = {
    # US Timezones
    'EST': 'US/Eastern',
    'EDT': 'US/Eastern', 
    'CST': 'US/Central',
    'CDT': 'US/Central',
    'MST': 'US/Mountain',
    'MDT': 'US/Mountain',
    'PST': 'US/Pacific',
    'PDT': 'US/Pacific',
    'AKST': 'US/Alaska',
    'AKDT': 'US/Alaska',
    'HST': 'US/Hawaii',
    'HDT': 'US/Hawaii',

    # European Timezones
    'GMT': 'GMT',
    'UTC': 'UTC',
    'BST': 'Europe/London',
    'CET': 'Europe/Paris',
    'CEST': 'Europe/Paris',
    'EET': 'Europe/Athens',
    'EEST': 'Europe/Athens',
    'WET': 'Europe/Lisbon',
    'WEST': 'Europe/Lisbon',

    # Asian Timezones
    'IST': 'Asia/Kolkata',
    'JST': 'Asia/Tokyo',
    'KST': 'Asia/Seoul',
    'CST': 'Asia/Shanghai',  # China Standard Time
    'SGT': 'Asia/Singapore',
    'HKT': 'Asia/Hong_Kong',
    'PKT': 'Asia/Karachi',
    'NPT': 'Asia/Kathmandu',
    'BDT': 'Asia/Dhaka',
    'LKT': 'Asia/Colombo',
    'MMT': 'Asia/Yangon',
    'ICT': 'Asia/Bangkok',
    'WIB': 'Asia/Jakarta',
    'WITA': 'Asia/Makassar',
    'WIT': 'Asia/Jayapura',
    'PHT': 'Asia/Manila',
    'MYT': 'Asia/Kuala_Lumpur',

    # Australian Timezones
    'AEST': 'Australia/Sydney',
    'AEDT': 'Australia/Sydney',
    'ACST': 'Australia/Adelaide',
    'ACDT': 'Australia/Adelaide',
    'AWST': 'Australia/Perth',
    'AWDT': 'Australia/Perth',

    # Other Common Timezones
    'CAT': 'Africa/Johannesburg',
    'EAT': 'Africa/Nairobi',
    'WAT': 'Africa/Lagos',
    'SAST': 'Africa/Johannesburg',
    'MSK': 'Europe/Moscow',
    'AST': 'America/Halifax',  # Atlantic Standard Time
    'ADT': 'America/Halifax',
    'NST': 'America/St_Johns',  # Newfoundland Standard Time
    'NDT': 'America/St_Johns',
    'BRT': 'America/Sao_Paulo',  # Brazil Time
    'ART': 'America/Argentina/Buenos_Aires',  # Argentina Time
    'CLT': 'America/Santiago',  # Chile Time
    'PET': 'America/Lima',  # Peru Time
    'COT': 'America/Bogota',  # Colombia Time
    'VET': 'America/Caracas',  # Venezuela Time
    'GYT': 'America/Guyana',  # Guyana Time
    'SRT': 'America/Paramaribo',  # Suriname Time
    'FNT': 'America/Noronha',  # Fernando de Noronha Time
    'NZST': 'Pacific/Auckland',  # New Zealand Standard Time
    'NZDT': 'Pacific/Auckland',
    'CHST': 'Pacific/Guam',  # Chamorro Standard Time
    'FJST': 'Pacific/Fiji',  # Fiji Standard Time
}


def resolve_timezone(timezone_input: str) -> str:
    """Resolve timezone abbreviation to IANA timezone name if needed."""
    if not timezone_input:
        return timezone_input

    # Check if it's already a valid IANA timezone
    try:
        ZoneInfo(timezone_input)
        return timezone_input
    except Exception:
        pass

    # Check if it's a timezone abbreviation
    timezone_upper = timezone_input.upper()
    if timezone_upper in TIMEZONE_ABBREVIATIONS:
        return TIMEZONE_ABBREVIATIONS[timezone_upper]

    # Return original input if no mapping found
    return timezone_input


def suggest_timezones(query: str) -> str:
    """Return a comma separated list of matching timezones."""
    try:
        # Special cases for common country names
        country_mappings = {
            'india': ['Asia/Kolkata', 'Asia/Calcutta', 'IST'],
            'usa': ['US/Eastern', 'US/Central', 'US/Mountain', 'US/Pacific', 'EST', 'CST', 'MST', 'PST'],
            'uk': ['Europe/London', 'GMT', 'BST'],
            'japan': ['Asia/Tokyo', 'JST'],
            'china': ['Asia/Shanghai', 'CST'],
            'australia': ['Australia/Sydney', 'Australia/Melbourne', 'AEST', 'ACST', 'AWST'],
        }

        query_lower = query.lower()
        if query_lower in country_mappings:
            return ", ".join(country_mappings[query_lower])

        # Check for timezone abbreviation matches
        abbreviation_matches = []
        for abbr, iana_name in TIMEZONE_ABBREVIATIONS.items():
            if query_lower in abbr.lower():
                abbreviation_matches.append(f"{abbr} ({iana_name})")

        # Fallback to substring matching in IANA timezones
        iana_matches = [tz for tz in available_timezones() if query_lower in tz.lower()]

        # Combine abbreviation and IANA matches
        all_matches = abbreviation_matches + iana_matches
        if not all_matches:
            return ""

        # Prioritize exact matches and common timezones
        exact_matches = [match for match in all_matches if query_lower == match.lower().split('/')[-1].split(' ')[0]]
        if exact_matches:
            all_matches = exact_matches + [match for match in all_matches if match not in exact_matches]

        return ", ".join(sorted(all_matches)[:5])
    except Exception:
        return ""


def display(dt_input: str | None, fmt: str, timezone: str | None) -> str:
    """Format the given datetime string in the requested timezone and format."""
    tz = None
    if timezone:
        # Resolve timezone abbreviation to IANA name if needed
        resolved_timezone = resolve_timezone(timezone)
        try:
            tz = ZoneInfo(resolved_timezone)
        except Exception as e:
            hint = suggest_timezones(timezone)
            msg = f"Invalid timezone: {timezone}"
            if hint:
                msg += f"\nDid you mean: {hint}?"
            msg += ("\nSee https://en.wikipedia.org/wiki/List_of_tz_database_time_zones"
                    " for a list of valid timezones.")
            PError(msg)
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


def current_time(timezone: str = "UTC") -> datetime:
    """Return current time in the given timezone."""
    # Resolve timezone abbreviation to IANA name if needed
    resolved_timezone = resolve_timezone(timezone)
    try:
        tz = ZoneInfo(resolved_timezone)
    except Exception as e:  # pragma: no cover - error should be very rare
        error(f"Invalid timezone: {timezone}\n{e}")
        raise
    return datetime.now(tz)


def convert(dt_str: str, from_tz: str, to_tz: str) -> datetime:
    """Convert ``dt_str`` from ``from_tz`` timezone to ``to_tz`` timezone."""
    # Resolve timezone abbreviations to IANA names if needed
    resolved_from_tz = resolve_timezone(from_tz)
    resolved_to_tz = resolve_timezone(to_tz)
    try:
        from_zone = ZoneInfo(resolved_from_tz)
        to_zone = ZoneInfo(resolved_to_tz)
    except Exception as e:  # pragma: no cover - user input error
        error(f"Invalid timezone provided\n{e}")
        raise
    dt = datetime.fromisoformat(dt_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=from_zone)
    else:
        dt = dt.astimezone(from_zone)
    return dt.astimezone(to_zone)
