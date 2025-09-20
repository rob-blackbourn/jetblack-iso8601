"""Serialization"""

from datetime import date, datetime, time, timezone, timedelta
import re
from typing import Optional

TZ_PART = r'(?P<zulu>Z)|((?P<tz_sign>[+-])(?P<tz_hours>\d{2}):?(?P<tz_minutes>\d{2}))'
TIME_PART = r'(?P<hours>\d{2}):(?P<minutes>\d{2}):(?P<seconds>\d{2})(\.(?P<fractions>\d+))?'
DATE_PART = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
TZ_PATTERN = re.compile(f'^{TZ_PART}$')
DATE_PATTERN = re.compile(f'^{DATE_PART}$')
TIME_PATTERN = re.compile(f'^{TIME_PART}$')
DATETIME_PATTERN = re.compile(f'^{DATE_PART}(T{TIME_PART}({TZ_PART})?)?$')


def iso8601_to_datetime(value: str) -> Optional[datetime]:
    """Parse an ISO 8601 datetime.

    Args:
        value (str): The ISO 8601 date string

    Returns:
        Optional[datetime]: A timestamp if the value could be parsed, otherwise
            None.
    """
    match = DATETIME_PATTERN.match(value)
    if match is None:
        return None

    parts = match.groupdict()

    year, month, day = (
        int(parts['year']), int(parts['month']), int(parts['day'])
    )

    hour, minute, second = (
        (0, 0, 0) if parts['hours'] is None
        else (
            int(parts['hours']), int(parts['minutes']), int(parts['seconds'])
        )
    )

    microsecond = (
        0 if parts['fractions'] is None
        else int(parts['fractions'][:6].ljust(6, '0'))
    )

    if parts['zulu']:
        tzinfo = timezone.utc
    elif parts['tz_sign']:
        offset = timedelta(
            hours=int(parts['tz_hours']),
            minutes=int(parts['tz_minutes'])
        )
        tzinfo = (
            timezone(offset) if parts['tz_sign'] == '+'
            else timezone(-offset)
        )
    else:
        tzinfo = None

    return datetime(
        year, month, day,
        hour, minute, second, microsecond,
        tzinfo
    )


def datetime_to_iso8601(timestamp: datetime) -> str:
    """Convert datetime to ISO 8601

    Args:
        timestamp (datetime): The timestamp

    Returns:
        str: The stringified ISO 8601 version of the timestamp
    """
    # pylint: disable=consider-using-f-string
    date_part = "{year:04d}-{month:02d}-{day:02d}".format(
        year=timestamp.year, month=timestamp.month, day=timestamp.day,
    )
    time_part = "{hour:02d}:{minute:02d}:{second:02d}.{millis:02d}".format(
        hour=timestamp.hour, minute=timestamp.minute, second=timestamp.second,
        millis=timestamp.microsecond // 1000
    )
    # pylint: enable=consider-using-f-string

    utcoffset = timestamp.utcoffset()
    if utcoffset is None or timestamp.tzinfo is timezone.utc:
        return f"{date_part}T{time_part}Z"

    tz_seconds = utcoffset.total_seconds()
    tz_sign = '-' if tz_seconds < 0 else '+'
    tz_minutes = int(abs(tz_seconds)) // 60
    tz_hours = tz_minutes // 60
    tz_minutes %= 60
    return f"{date_part}T{time_part}{tz_sign}{tz_hours:02d}:{tz_minutes:02d}"


def iso8601_to_date(value: str) -> Optional[date]:
    """Parse an ISO 8601 date.

    Args:
        value (str): The ISO 8601 date string

    Returns:
        Optional[date]: A timestamp if the value could be parsed, otherwise
            None.
    """
    match = DATE_PATTERN.match(value)
    if match is None:
        return None

    parts = match.groupdict()

    year, month, day = (
        int(parts['year']), int(parts['month']), int(parts['day'])
    )

    return date(year, month, day)


def date_to_iso8601(value: date) -> str:
    """Convert date to ISO 8601

    Args:
        value (date): The date

    Returns:
        str: The stringified ISO 8601 version of the date
    """
    # pylint: disable=consider-using-f-string
    return "{year:04d}-{month:02d}-{day:02d}".format(
        year=value.year, month=value.month, day=value.day,
    )


def iso8601_to_time(value: str) -> Optional[time]:
    """Parse an ISO 8601 time.

    Args:
        value (str): The ISO 8601 time string

    Returns:
        Optional[datetime]: A time if the value could be parsed, otherwise
            None.
    """
    match = TIME_PATTERN.match(value)
    if match is None:
        return None

    parts = match.groupdict()

    hour, minute, second = (
        int(parts['hours']), int(parts['minutes']), int(parts['seconds'])
    )

    microsecond = (
        0 if parts['fractions'] is None
        else int(parts['fractions'][:6].ljust(6, '0'))
    )

    return time(hour, minute, second, microsecond)


def time_to_iso8601(value: time, *, ndigits: int = 0) -> str:
    """Convert time to ISO 8601

    Args:
        value (time): The time
        ndigits_millis (int): The number of digits of fractional seconds to include.
            Default is 0, which means none are included.

    Returns:
        str: The stringified ISO 8601 version of the time
    """
    # pylint: disable=consider-using-f-string
    text = "{hour:02d}:{minute:02d}:{second:02d}".format(
        hour=value.hour, minute=value.minute, second=value.second
    )
    # pylint: enable=consider-using-f-string

    if ndigits > 0:
        millis = str(value.microsecond).rjust(6, '0')[:ndigits]
        text = f"{text}.{millis}"

    return text


def iso8601_to_timezone(value: str) -> Optional[timezone]:
    """Parse an ISO 8601 timezone.

    Args:
        value (str): The ISO 8601 timezone

    Returns:
        Optional[datetime]: A timezone if the value could be parsed, otherwise
            None.
    """
    match = TZ_PATTERN.match(value)
    if match is None:
        return None

    parts = match.groupdict()

    if parts['zulu']:
        tzinfo = timezone.utc
    elif parts['tz_sign']:
        offset = timedelta(
            hours=int(parts['tz_hours']),
            minutes=int(parts['tz_minutes'])
        )
        tzinfo = (
            timezone(offset) if parts['tz_sign'] == '+'
            else timezone(-offset)
        )
    else:
        tzinfo = None

    return tzinfo


def timezone_to_iso8601(tzinfo: timezone) -> str:
    """Convert timezone to ISO 8601

    Args:
        tzinfo (datetime): The timezone

    Returns:
        str: The stringified ISO 8601 version of the timezone
    """
    utcoffset = tzinfo.utcoffset(None)
    if utcoffset is None or tzinfo is timezone.utc:
        return "Z"

    tz_seconds = utcoffset.total_seconds()
    tz_sign = '-' if tz_seconds < 0 else '+'
    tz_minutes = int(abs(tz_seconds)) // 60
    tz_hours = tz_minutes // 60
    tz_minutes %= 60
    return f"{tz_sign}{tz_hours:02d}:{tz_minutes:02d}"
