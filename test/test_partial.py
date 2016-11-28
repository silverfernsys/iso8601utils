import pytest


from datetime import datetime, timedelta, date
from iso8601utils.tz import utc
from iso8601utils.helpers.builder import (datetime_builder, datetime_builder_partial,
    date_builder_partial, interval_datetimes_builder)
from iso8601utils.validators import _datetime_partial, _datetime_strict


def test_validators():
    assert _datetime_strict('2005-03-20T05:15+03:00') == True
    assert _datetime_partial('23T17:00') == True

    assert _datetime_strict('2007-11-13') == True
    assert _datetime_partial('15') == True

    assert _datetime_strict('2007-11-13T09:00') == True
    assert _datetime_partial('15T17:00') == True

def test_partial():
    s = datetime(2007, 11, 13, 0, 0, tzinfo=utc)
    a = date_builder_partial('15', s)
    assert a == date(2007, 11, 15)
    e = datetime_builder_partial('15', timedelta(1), s)
    assert e == datetime(2007, 11, 16, 0, 0, tzinfo=utc)

def test_builder():
    (s, e) = interval_datetimes_builder('2007-11-13', '15')
    assert s == datetime(2007, 11, 13, 0, 0, tzinfo=utc)
    assert e == datetime(2007, 11, 16, 0, 0, tzinfo=utc)

    (s, e) = interval_datetimes_builder('2007-11-13T09:00', '15T17:00')
    assert s == datetime(2007, 11, 13, 9, 0, tzinfo=utc)
    assert e == datetime(2007, 11, 15, 17, 0, tzinfo=utc)

    (s, e) = interval_datetimes_builder('2007-12-14T13:30', '15:30')
    assert s == datetime(2007, 12, 14, 13, 30, tzinfo=utc)
    assert e == datetime(2007, 12, 14, 15, 30, tzinfo=utc)
