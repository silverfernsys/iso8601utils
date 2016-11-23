import pytest


from datetime import timedelta
from iso8601utils.tz import timezone


def test_tz():
    tz = timezone()
    assert tz.offset == timedelta(hours=0, minutes=0)
    assert tz.hours == 0
    assert tz.minutes == 0
    assert tuple(tz) == (0, 0)
    assert tz.name == tz.tzname(None)
    assert tz.dst(None) == timedelta(0)
    assert tz.utcoffset(None) == timedelta(0)
    assert tz.__repr__() == '+00:00'
    assert str(tz) == '+00:00'

    tz = -timezone(hours=5, minutes=20)
    assert tz.hours == -5
    assert tz.minutes == -20
    assert tuple(tz) == (-5, -20)
    assert tz.name == tz.tzname(None)
    assert tz.dst(None) == timedelta(0)
    assert tz.utcoffset(None) == -timedelta(hours=5, minutes=20)
    assert tz.__repr__() == '-05:20'
    assert str(tz) == '-05:20'

    tz = -timezone(hours=4, minutes=30, name='test')
    assert tz.hours == -4
    assert tz.minutes == -30
    assert tuple(tz) == (-4, -30)
    assert tz.name == 'test'
    assert tz.name == tz.tzname(None)
    assert tz.dst(None) == timedelta(0)
    assert tz.utcoffset(None) == -timedelta(hours=4, minutes=30)
    assert tz.__repr__() == 'test'
    assert str(tz) == 'test'
