"""Tests for duration"""

from jetblack_iso8601.duration import (
    iso8601_to_timedelta,
    timedelta_to_iso8601
)


def test_full_with_days():
    """Test duration"""

    duration = 'P3Y2M1DT12H11M10S'
    value = iso8601_to_timedelta(duration)
    roundtrip = timedelta_to_iso8601(value)
    assert roundtrip == duration


def test_full_with_weeks():
    """Test duration"""

    duration = 'P3Y2M1WT12H11M10S'
    value = iso8601_to_timedelta(duration)
    roundtrip = timedelta_to_iso8601(value)
    assert roundtrip == duration


def test_date_only():
    """Test duration"""

    duration = 'P3Y2M1D'
    value = iso8601_to_timedelta(duration)
    roundtrip = timedelta_to_iso8601(value)
    assert roundtrip == duration


def test_time_only():
    """Test duration"""

    duration = 'PT12H11M10S'
    value = iso8601_to_timedelta(duration)
    roundtrip = timedelta_to_iso8601(value)
    assert roundtrip == duration


def test_negative():
    """Test duration"""

    duration = '-PT10M'
    value = iso8601_to_timedelta(duration)
    roundtrip = timedelta_to_iso8601(value)
    assert roundtrip == duration


def test_empty():
    """Test duration"""

    duration = '-P0Y0M0DT0H0M0S'
    value = iso8601_to_timedelta(duration)
    roundtrip = timedelta_to_iso8601(value)
    assert roundtrip == 'P0D'
