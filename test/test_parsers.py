import pytest

from monthdelta import MonthDelta as monthdelta
from datetime import datetime as datetime_, timedelta, time as time_, date as date_
from iso8601utils import parsers, interval, duration
from iso8601utils.tz import timezone, utc


def test_time():
    with pytest.raises(ValueError):
        parsers.time('1234a')
       
    with pytest.raises(ValueError):
        parsers.time('1234a')

    with pytest.raises(ValueError):
        parsers.time('12:30:40.05+0:15')

    with pytest.raises(ValueError):
        parsers.time('1230401.05+10:15')

    with pytest.raises(ValueError):
        parsers.time('24:00:00.0001')

    assert parsers.time('24:00:00') == parsers.time('00:00:00')
    assert parsers.time('12') == time_(hour=12, tzinfo=utc)
    assert parsers.time('12+05:10') == time_(hour=12, tzinfo=timezone(hours=5, minutes=10))
    assert parsers.time('12-05:10') == time_(hour=12, tzinfo=-timezone(hours=5, minutes=10))
    assert parsers.time('13:15') == time_(hour=13, minute=15, tzinfo=utc)
    assert parsers.time('13:15+05:10') == time_(hour=13, minute=15, tzinfo=timezone(hours=5, minutes=10))
    assert parsers.time('13:15-05:10') == time_(hour=13, minute=15, tzinfo=-timezone(hours=5, minutes=10))
    assert parsers.time('14:20:50') == time_(hour=14, minute=20, second=50, tzinfo=utc)
    assert parsers.time('14:20:50+05:10') == time_(hour=14, minute=20, second=50, tzinfo=timezone(hours=5, minutes=10))
    assert parsers.time('14:20:50-05:10') == time_(hour=14, minute=20, second=50, tzinfo=-timezone(hours=5, minutes=10))
    assert parsers.time('14:20:50+05') == time_(hour=14, minute=20, second=50, tzinfo=timezone(hours=5))
    assert parsers.time('14:20:50-05') == time_(hour=14, minute=20, second=50, tzinfo=-timezone(hours=5))
    assert parsers.time('14:20:50+0510') == time_(hour=14, minute=20, second=50, tzinfo=timezone(hours=5, minutes=10))
    assert parsers.time('14:20:50-0510') == time_(hour=14, minute=20, second=50, tzinfo=-timezone(hours=5, minutes=10))
    assert parsers.time('12:30:40.05') == time_(hour=12, minute=30, second=40, microsecond=5000, tzinfo=utc)
    assert parsers.time('12:30:40.05Z') == time_(hour=12, minute=30, second=40, microsecond=5000, tzinfo=utc)
    assert parsers.time('12:30:40.05+10:15') == time_(hour=12, minute=30, second=40, microsecond=5000, tzinfo=timezone(hours=10, minutes=15))
    assert parsers.time('12:30:40.05-08:45') == time_(hour=12, minute=30, second=40, microsecond=5000, tzinfo=-timezone(hours=8, minutes=45))
    assert parsers.time('1315') == time_(hour=13, minute=15, tzinfo=utc)
    assert parsers.time('1315+05:10') == time_(hour=13, minute=15, tzinfo=timezone(hours=5, minutes=10))
    assert parsers.time('1315-05:10') == time_(hour=13, minute=15, tzinfo=-timezone(hours=5, minutes=10))
    assert parsers.time('142050'), time_(hour=14, minute=20, second=50, tzinfo=utc)
    assert parsers.time('142050+05:10') == time_(hour=14, minute=20, second=50, tzinfo=timezone(hours=5, minutes=10))
    assert parsers.time('142050-05:10') == time_(hour=14, minute=20, second=50, tzinfo=-timezone(hours=5, minutes=10))
    assert parsers.time('142050+05') == time_(hour=14, minute=20, second=50, tzinfo=timezone(hours=5))
    assert parsers.time('142050-05') == time_(hour=14, minute=20, second=50, tzinfo=-timezone(hours=5))
    assert parsers.time('142050+0510') == time_(hour=14, minute=20, second=50, tzinfo=timezone(hours=5, minutes=10))
    assert parsers.time('142050-0510') == time_(hour=14, minute=20, second=50, tzinfo=-timezone(hours=5, minutes=10))
    assert parsers.time('123040.05') == time_(hour=12, minute=30, second=40, microsecond=5000, tzinfo=utc)
    assert parsers.time('123040.05Z') == time_(hour=12, minute=30, second=40, microsecond=5000, tzinfo=utc)
    assert parsers.time('123040.05+10:15') == time_(hour=12, minute=30, second=40, microsecond=5000, tzinfo=timezone(hours=10, minutes=15))
    assert parsers.time('123040.05-08:45') == time_(hour=12, minute=30, second=40, microsecond=5000, tzinfo=-timezone(hours=8, minutes=45))

def test_date():
    assert parsers.date('2005-01-01') == parsers.date('2004-W53-6')  
    assert parsers.date('2005-01-02') == parsers.date('2004-W53-7')
    assert parsers.date('2005-12-31') == parsers.date('2005-W52-6')
    assert parsers.date('2007-01-01') == parsers.date('2007-W01-1')
    assert parsers.date('2007-12-30') == parsers.date('2007-W52-7')
    assert parsers.date('2007-12-31') == parsers.date('2008-W01-1')
    assert parsers.date('2008-01-01') == parsers.date('2008-W01-2')
    assert parsers.date('2008-12-28') == parsers.date('2008-W52-7')
    assert parsers.date('2008-12-29') == parsers.date('2009-W01-1')
    assert parsers.date('2008-12-30') == parsers.date('2009-W01-2')
    assert parsers.date('2008-12-31') == parsers.date('2009-W01-3')
    assert parsers.date('2009-01-01') == parsers.date('2009-W01-4')
    assert parsers.date('2009-12-31') == parsers.date('2009-W53-4')
    assert parsers.date('2010-01-01') == parsers.date('2009-W53-5')
    assert parsers.date('2010-01-02') == parsers.date('2009-W53-6')
    assert parsers.date('2010-01-03') == parsers.date('2009-W53-7')
    assert parsers.date('2008-W39-6') == date_(2008, 9, 27)
    assert parsers.date('2008W396') == date_(2008, 9, 27)
    assert parsers.date('2016W431') == date_(2016, 10, 24)
    assert parsers.date('2016-W43-1') == date_(2016, 10, 24)
    assert parsers.date('2015-W30-4') == date_(2015, 7, 23)
    assert parsers.date('1981-095') == date_(1981, 4, 5)
    assert parsers.date('1981095') == date_(1981, 4, 5)
    assert parsers.date('1981-04-05') == date_(1981, 4, 5)
    assert parsers.date('19810405') == date_(1981, 4, 5)
    assert parsers.date('--04-03') == date_(1, 4, 3)
    assert parsers.date('--1001') == date_(1, 10, 1)

    with pytest.raises(ValueError):
        parsers.date('2008-W396')

    with pytest.raises(ValueError):
        parsers.date('2008W39-6')

    with pytest.raises(ValueError):
        parsers.date('198195')

    with pytest.raises(ValueError):
        parsers.date('1981-0405')

    with pytest.raises(ValueError):
        parsers.date('198104-05')

def test_datetime():
    assert parsers.datetime('2007-04-05T14:30') == datetime_(2007, 4, 5, 14, 30, tzinfo=utc)
    assert parsers.datetime('2007-08-09T12:30Z') == datetime_(2007, 8, 9, 12, 30, tzinfo=utc)
    assert parsers.datetime('2007-01-01T24:00:00') == datetime_(2007, 1, 2, 0, 0, 0, tzinfo=utc)
    assert parsers.datetime('2007-01-01T24:00:00') == parsers.datetime('2007-01-02T00:00:00')
    assert parsers.datetime('2007-08-09T12:30-02:00') == datetime_(2007, 8, 9, 12, 30,
        tzinfo=-timezone(hours=2, minutes=0))

    with pytest.raises(ValueError):
        parsers.datetime('invalid')

def test_interval():
    now = datetime_(2016, 1, 1)
    with pytest.raises(ValueError):
        parsers.interval('P6Yasdf')

    with pytest.raises(ValueError):
        parsers.interval('7432891')

    with pytest.raises(ValueError):
        parsers.interval('asdf')

    with pytest.raises(ValueError):
        parsers.interval('23P7DT5H')

    with pytest.raises(ValueError):
        parsers.interval('1999-12-31T16:00:00.000Z')

    with pytest.raises(ValueError):
        parsers.interval('1999-12-31T16:00:00.000+08:30')

    with pytest.raises(ValueError):
        parsers.interval('P6Yasdf/P8Y')

    with pytest.raises(ValueError):
        parsers.interval('P7Y/asdf')

    with pytest.raises(ValueError):
        parsers.interval('1999-12-01T00:00:0a/1999-12-31T16:00:00.000Z')

    with pytest.raises(ValueError):
        parsers.interval('A4/1999-12-01T00:00:00/1999-12-31T16:00:00.000Z')

    with pytest.raises(ValueError):
        parsers.interval('P6Y5M/P9D')

    with pytest.raises(ValueError):
        parsers.interval('7432891/1234')

    with pytest.raises(ValueError):
        parsers.interval('asdf/87rf')

    with pytest.raises(ValueError):
        parsers.interval('23P7DT5H/89R3')

    assert parsers.interval('P7Y', now=now) == interval(end=now, duration=duration(years=7))
    assert parsers.interval('P6W', now=now) == interval(end=now, duration=duration(weeks=6))
    assert parsers.interval('R1/P6Y5M', now=now) == interval(end=now, repeats=1, duration=duration(years=6, months=5))
    assert parsers.interval('R5/1999-12-31T16:00:00.000Z/P5DT7H') == interval(start=datetime_(year=1999, month=12, day=31,
        hour=16, tzinfo=utc), duration=duration(days=5, hours=7), repeats=5)
    assert parsers.interval('R7/2016-08-01T23:10:59.111Z/2016-08-08T00:13:23.001Z') == interval(start=datetime_(year=2016,
        month=8, day=1, hour=23, minute=10, second=59, microsecond=111000, tzinfo=utc), end=datetime_(year=2016, month=8,
        day=8, hour=0, minute=13, second=23, microsecond=1000, tzinfo=utc), repeats=7)
    assert parsers.interval('R2/P5DT7H/1999-12-31T16:00:00.000Z') == interval(end=datetime_(year=1999, month=12, day=31,
        hour=16, tzinfo=utc), duration=duration(days=5, hours=7), repeats=2)
    assert parsers.interval('R5/2002-08-15T16:20:05.100+08:10/P5DT7H') == interval(start=datetime_(year=2002, month=8,
        day=15, hour=16, minute=20, second=5, microsecond=100000, tzinfo=timezone(hours=8, minutes=10)),
        duration=duration(days=5, hours=7), repeats=5)
    assert parsers.interval('2002-08-15T16:20:05.100+08:10/2002-10-12T17:05:25.020-01:40') == interval(start=datetime_(year=2002, 
        month=8, day=15, hour=16, minute=20, second=5, microsecond=100000, tzinfo=timezone(hours=8, minutes=10)),
        end=datetime_(year=2002, month=10, day=12, hour=17, minute=5, second=25, microsecond=20000,
            tzinfo=-timezone(hours=1, minutes=40)))
    assert parsers.interval('R/P5DT7H/2002-08-15T16:20:05.100+08:10') == interval(end=datetime_(year=2002, month=8,
        day=15, hour=16, minute=20, second=5, microsecond=100000, tzinfo=timezone(hours=8, minutes=10)),
        duration=duration(days=5, hours=7), repeats=float('inf'))

def test_partial_intervals():
    assert parsers.interval('2005-03-20T05:15+03:00/23T17:00') == interval(repeats=0, start=datetime_(2005, 3, 20, 5, 15,
        tzinfo=timezone(hours=3, minutes=0)), end=datetime_(2005, 3, 23, 17, tzinfo=timezone(hours=3, minutes=0)))
    assert parsers.interval('2007-11-13/15') == interval(repeats=0, start=datetime_(2007, 11, 13, tzinfo=utc),
        end=datetime_(2007, 11, 16, tzinfo=utc))
    assert parsers.interval('2007-11-13T09:00/15T17:00') == interval(repeats=0, start=datetime_(2007, 11, 13, 9, tzinfo=utc),
        end=datetime_(2007, 11, 15, 17, tzinfo=utc))

def test_duration():
    assert parsers.duration('P3Y6M4DT12H30M5S') == duration(timedelta=timedelta(days=4, hours=12,
        minutes=30, seconds=5), monthdelta=monthdelta(6 + 3 * 12))
    assert parsers.duration('P6M4DT12H30M15S') == duration(timedelta=timedelta(days=4, hours=12,
        minutes=30, seconds=15), monthdelta=monthdelta(6))
    assert parsers.duration('P6M1DT') == duration(timedelta=timedelta(days=1), monthdelta=monthdelta(6))
    assert parsers.duration('P6W') == duration(timedelta=timedelta(weeks=6), monthdelta=monthdelta(0))
    assert parsers.duration('P0.5W') == duration(timedelta=timedelta(weeks=0.5), monthdelta=monthdelta(0))
    assert parsers.duration('P5M3DT5S') == duration(timedelta=timedelta(days=3, seconds=5), monthdelta=monthdelta(5))
    assert parsers.duration('P3Y4DT12H5S') == duration(timedelta=timedelta(days=4, hours=12, seconds=5),
        monthdelta=monthdelta(3 * 12))
    assert parsers.duration('P3Y4DT12H30M0.5005S') == duration(timedelta=timedelta(days=4, hours=12, minutes=30, 
        milliseconds=500, microseconds=500), monthdelta=monthdelta(3 * 12))
    assert parsers.duration('PT.5005S') == duration(timedelta=timedelta(milliseconds=500, microseconds=500),
        monthdelta=monthdelta(0))
    assert parsers.duration('P10W') == duration(timedelta=timedelta(weeks=10), monthdelta=monthdelta(0))
    assert parsers.duration('P7W') == duration(timedelta=timedelta(weeks=7), monthdelta=monthdelta(0))
    assert parsers.duration('P0003-06-04T12:30:05') == duration(timedelta=timedelta(days=4, hours=12, minutes=30,
        seconds=5), monthdelta=monthdelta(6 + 3 * 12))
    assert parsers.duration('P00200907T114515') == duration(timedelta=timedelta(days=7, hours=11, minutes=45, seconds=15),
        monthdelta=monthdelta(9 + 20 * 12))
    
    with pytest.raises(ValueError):
        parsers.duration('P6Yasdf')

    with pytest.raises(ValueError):
        parsers.duration('7432891')

    with pytest.raises(ValueError):
        parsers.duration('asdf')

    with pytest.raises(ValueError):
        parsers.duration('23P7DT5H')

    with pytest.raises(ValueError):
        parsers.duration('')
