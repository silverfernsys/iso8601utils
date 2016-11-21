import unittest

try:
    import mock
except:
    from unittest import mock

from monthdelta import MonthDelta as monthdelta
from datetime import datetime as datetime_, timedelta, time as time_, date as date_
from iso8601utils import parsers, interval, duration
from iso8601utils.tz import TimezoneInfo, utc


class TestParsers(unittest.TestCase):
    def test_time(self):
        self.assertRaises(ValueError, parsers.time, '1234a')
        self.assertRaises(ValueError, parsers.time, '12:30:40.05+0:15')
        self.assertRaises(ValueError, parsers.time, '1230401.05+10:15')
        self.assertRaises(ValueError, parsers.time, '24:00:00.0001')
        self.assertEqual(parsers.time('24:00:00'), parsers.time('00:00:00'))
        self.assertEqual(parsers.time('12'), time_(hour=12, tzinfo=utc))
        self.assertEqual(parsers.time('12+05:10'), time_(hour=12, tzinfo=TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(parsers.time('12-05:10'), time_(hour=12, tzinfo=-TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(parsers.time('13:15'), time_(hour=13, minute=15, tzinfo=utc))
        self.assertEqual(parsers.time('13:15+05:10'),
            time_(hour=13, minute=15, tzinfo=TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(parsers.time('13:15-05:10'),
            time_(hour=13, minute=15, tzinfo=-TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(parsers.time('14:20:50'), time_(hour=14, minute=20, second=50, tzinfo=utc))
        self.assertEqual(parsers.time('14:20:50+05:10'),
            time_(hour=14, minute=20, second=50, tzinfo=TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(parsers.time('14:20:50-05:10'),
            time_(hour=14, minute=20, second=50, tzinfo=-TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(parsers.time('14:20:50+05'),
            time_(hour=14, minute=20, second=50, tzinfo=TimezoneInfo(hours=5)))
        self.assertEqual(parsers.time('14:20:50-05'),
            time_(hour=14, minute=20, second=50, tzinfo=-TimezoneInfo(hours=5)))
        self.assertEqual(parsers.time('14:20:50+0510'),
            time_(hour=14, minute=20, second=50, tzinfo=TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(parsers.time('14:20:50-0510'),
            time_(hour=14, minute=20, second=50, tzinfo=-TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(parsers.time('12:30:40.05'), time_(hour=12, minute=30, second=40, microsecond=5000, tzinfo=utc))
        self.assertEqual(parsers.time('12:30:40.05Z'), time_(hour=12, minute=30, second=40, microsecond=5000, tzinfo=utc))
        self.assertEqual(parsers.time('12:30:40.05+10:15'),
            time_(hour=12, minute=30, second=40, microsecond=5000, tzinfo=TimezoneInfo(hours=10, minutes=15)))
        self.assertEqual(parsers.time('12:30:40.05-08:45'),
            time_(hour=12, minute=30, second=40, microsecond=5000, tzinfo=-TimezoneInfo(hours=8, minutes=45)))
        self.assertEqual(parsers.time('1315'), time_(hour=13, minute=15, tzinfo=utc))
        self.assertEqual(parsers.time('1315+05:10'),
            time_(hour=13, minute=15, tzinfo=TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(parsers.time('1315-05:10'),
            time_(hour=13, minute=15, tzinfo=-TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(parsers.time('142050'), time_(hour=14, minute=20, second=50, tzinfo=utc))
        self.assertEqual(parsers.time('142050+05:10'),
            time_(hour=14, minute=20, second=50, tzinfo=TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(parsers.time('142050-05:10'),
            time_(hour=14, minute=20, second=50, tzinfo=-TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(parsers.time('142050+05'),
            time_(hour=14, minute=20, second=50, tzinfo=TimezoneInfo(hours=5)))
        self.assertEqual(parsers.time('142050-05'),
            time_(hour=14, minute=20, second=50, tzinfo=-TimezoneInfo(hours=5)))
        self.assertEqual(parsers.time('142050+0510'),
            time_(hour=14, minute=20, second=50, tzinfo=TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(parsers.time('142050-0510'),
            time_(hour=14, minute=20, second=50, tzinfo=-TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(parsers.time('123040.05'), time_(hour=12, minute=30, second=40, microsecond=5000, tzinfo=utc))
        self.assertEqual(parsers.time('123040.05Z'), time_(hour=12, minute=30, second=40, microsecond=5000, tzinfo=utc))
        self.assertEqual(parsers.time('123040.05+10:15'),
            time_(hour=12, minute=30, second=40, microsecond=5000, tzinfo=TimezoneInfo(hours=10, minutes=15)))
        self.assertEqual(parsers.time('123040.05-08:45'),
            time_(hour=12, minute=30, second=40, microsecond=5000, tzinfo=-TimezoneInfo(hours=8, minutes=45)))

    def test_date(self):
        self.assertEqual(parsers.date('2005-01-01'), parsers.date('2004-W53-6'))  
        self.assertEqual(parsers.date('2005-01-02'), parsers.date('2004-W53-7'))
        self.assertEqual(parsers.date('2005-12-31'), parsers.date('2005-W52-6'))
        self.assertEqual(parsers.date('2007-01-01'), parsers.date('2007-W01-1'))
        self.assertEqual(parsers.date('2007-12-30'), parsers.date('2007-W52-7'))
        self.assertEqual(parsers.date('2007-12-31'), parsers.date('2008-W01-1'))
        self.assertEqual(parsers.date('2008-01-01'), parsers.date('2008-W01-2'))
        self.assertEqual(parsers.date('2008-12-28'), parsers.date('2008-W52-7'))
        self.assertEqual(parsers.date('2008-12-29'), parsers.date('2009-W01-1'))
        self.assertEqual(parsers.date('2008-12-30'), parsers.date('2009-W01-2'))
        self.assertEqual(parsers.date('2008-12-31'), parsers.date('2009-W01-3'))
        self.assertEqual(parsers.date('2009-01-01'), parsers.date('2009-W01-4'))
        self.assertEqual(parsers.date('2009-12-31'), parsers.date('2009-W53-4'))
        self.assertEqual(parsers.date('2010-01-01'), parsers.date('2009-W53-5'))
        self.assertEqual(parsers.date('2010-01-02'), parsers.date('2009-W53-6'))
        self.assertEqual(parsers.date('2010-01-03'), parsers.date('2009-W53-7'))
        self.assertEqual(parsers.date('2008-W39-6'), date_(2008, 9, 27))
        self.assertEqual(parsers.date('2008W396'), date_(2008, 9, 27))
        self.assertEqual(parsers.date('2016W431'), date_(2016, 10, 24))
        self.assertEqual(parsers.date('2016-W43-1'), date_(2016, 10, 24))
        self.assertEqual(parsers.date('2015-W30-4'), date_(2015, 7, 23))
        self.assertEqual(parsers.date('1981-095'), date_(1981, 4, 5))
        self.assertEqual(parsers.date('1981095'), date_(1981, 4, 5))
        self.assertEqual(parsers.date('1981-04-05'), date_(1981, 4, 5))
        self.assertEqual(parsers.date('19810405'), date_(1981, 4, 5))
        self.assertEqual(parsers.date('--04-03'), date_(1, 4, 3))
        self.assertEqual(parsers.date('--1001'), date_(1, 10, 1))
        self.assertRaises(ValueError, parsers.date, '2008-W396')
        self.assertRaises(ValueError, parsers.date, '2008W39-6')
        self.assertRaises(ValueError, parsers.date, '198195')
        self.assertRaises(ValueError, parsers.date, '1981-0405')
        self.assertRaises(ValueError, parsers.date, '198104-05')

    def test_datetime(self):
        self.assertEqual(parsers.datetime('2007-04-05T14:30'), datetime_(2007, 4, 5, 14, 30, tzinfo=utc))
        self.assertEqual(parsers.datetime('2007-08-09T12:30Z'), datetime_(2007, 8, 9, 12, 30, tzinfo=utc))
        self.assertEqual(parsers.datetime('2007-01-01T24:00:00'), datetime_(2007, 1, 2, 0, 0, 0, tzinfo=utc))
        self.assertEqual(parsers.datetime('2007-01-01T24:00:00'), parsers.datetime('2007-01-02T00:00:00'))
        self.assertEqual(parsers.datetime('2007-08-09T12:30-02:00'),
            datetime_(2007, 8, 9, 12, 30, tzinfo=-TimezoneInfo(hours=2, minutes=0)))
        self.assertRaises(ValueError, parsers.datetime, 'invalid')

    def test_interval(self):
        now = datetime_(2016, 1, 1)
        self.assertRaises(ValueError, parsers.interval, 'P6Yasdf')
        self.assertRaises(ValueError, parsers.interval, '7432891')
        self.assertRaises(ValueError, parsers.interval, 'asdf')
        self.assertRaises(ValueError, parsers.interval, '23P7DT5H')
        self.assertRaises(ValueError, parsers.interval, '1999-12-31T16:00:00.000Z')
        self.assertRaises(ValueError, parsers.interval, '1999-12-31T16:00:00.000+08:30')
        self.assertRaises(ValueError, parsers.interval, 'P6Yasdf/P8Y')
        self.assertRaises(ValueError, parsers.interval, 'P7Y/asdf')
        self.assertRaises(ValueError, parsers.interval, '1999-12-01T00:00:0a/1999-12-31T16:00:00.000Z')
        self.assertRaises(ValueError, parsers.interval, 'A4/1999-12-01T00:00:00/1999-12-31T16:00:00.000Z')
        self.assertRaises(ValueError, parsers.interval, 'P6Y5M/P9D')
        self.assertRaises(ValueError, parsers.interval, '7432891/1234')
        self.assertRaises(ValueError, parsers.interval, 'asdf/87rf')
        self.assertRaises(ValueError, parsers.interval, '23P7DT5H/89R3')

        # self.assertEqual(interval('2007-11-13/15'), Interval(0, datetime(2007, 11, 13), datetime(2007, 11, 16),
        #     (timedelta(days=3), monthdelta(0))))
        # self.assertEqual(interval('2007-11-13T09:00/15T17:00'), Interval(0, datetime(2007, 11, 13), datetime(2007, 11, 15, 17),
        #     (timedelta(days=2, hours=8), monthdelta(0))))
        # self.assertEqual(interval('2005-03-20T5:15+03:00/23T17:00'), Interval(0, datetime(2005, 3, 20, 5, 15,
        #     tzinfo=TimezoneInfo(hours=3, minutes=0)), datetime(2005, 3, 23, 17, tzinfo=TimezoneInfo(hours=3, minutes=0)),
        #     (timedelta(days=2, hours=17), monthdelta(0))))

        self.assertEqual(parsers.interval('P7Y', now=now), interval(end=now, duration=duration(years=7)))
        self.assertEqual(parsers.interval('P6W', now=now), interval(end=now, duration=duration(weeks=6)))
        self.assertEqual(parsers.interval('R1/P6Y5M', now=now),
            interval(end=now, repeats=1, duration=duration(years=6, months=5)))
        self.assertEqual(parsers.interval('R5/1999-12-31T16:00:00.000Z/P5DT7H'),
            interval(start=datetime_(year=1999, month=12, day=31, hour=16, tzinfo=utc), duration=duration(days=5, hours=7), repeats=5))
        self.assertEqual(parsers.interval('R7/2016-08-01T23:10:59.111Z/2016-08-08T00:13:23.001Z'),
            interval(start=datetime_(year=2016, month=8, day=1, hour=23, minute=10, second=59, microsecond=111000, tzinfo=utc),
                end=datetime_(year=2016, month=8, day=8, hour=0, minute=13, second=23, microsecond=1000, tzinfo=utc), repeats=7))
        self.assertEqual(parsers.interval('R2/P5DT7H/1999-12-31T16:00:00.000Z'),
            interval(end=datetime_(year=1999, month=12, day=31, hour=16, tzinfo=utc), duration=duration(days=5, hours=7),
                repeats=2))
        self.assertEqual(parsers.interval('R5/2002-08-15T16:20:05.100+08:10/P5DT7H'),
            interval(start=datetime_(year=2002, month=8, day=15, hour=16, minute=20, second=5, microsecond=100000,
                    tzinfo=TimezoneInfo(hours=8, minutes=10)), duration=duration(days=5, hours=7), repeats=5))
        self.assertEqual(parsers.interval('2002-08-15T16:20:05.100+08:10/2002-10-12T17:05:25.020-01:40'),
            interval(start=datetime_(year=2002, month=8, day=15, hour=16, minute=20, second=5, microsecond=100000,
                    tzinfo=TimezoneInfo(hours=8, minutes=10)),
                end=datetime_(year=2002, month=10, day=12, hour=17, minute=5, second=25, microsecond=20000,
                    tzinfo=-TimezoneInfo(hours=1, minutes=40))))
        self.assertEqual(parsers.interval('R/P5DT7H/2002-08-15T16:20:05.100+08:10'),
            interval(end=datetime_(year=2002, month=8, day=15, hour=16, minute=20, second=5,
                microsecond=100000, tzinfo=TimezoneInfo(hours=8, minutes=10)), duration=duration(days=5, hours=7), repeats=float('inf')))

    def test_duration(self):
        self.assertEqual(parsers.duration('P3Y6M4DT12H30M5S'),
                         duration(timedelta=timedelta(days=4, hours=12, minutes=30, seconds=5),
                            monthdelta=monthdelta(6 + 3 * 12)))
        self.assertEqual(parsers.duration('P6M4DT12H30M15S'),
                         duration(timedelta=timedelta(days=4, hours=12, minutes=30, seconds=15),
                            monthdelta=monthdelta(6)))
        self.assertEqual(parsers.duration('P6M1DT'),
                         duration(timedelta=timedelta(days=1), monthdelta=monthdelta(6)))
        self.assertEqual(parsers.duration('P6W'),
                         duration(timedelta=timedelta(weeks=6), monthdelta=monthdelta(0)))
        self.assertEqual(parsers.duration('P0.5W'),
                         duration(timedelta=timedelta(weeks=0.5), monthdelta=monthdelta(0)))
        self.assertEqual(parsers.duration('P5M3DT5S'),
                         duration(timedelta=timedelta(days=3, seconds=5), monthdelta=monthdelta(5)))
        self.assertEqual(parsers.duration('P3Y4DT12H5S'),
                         duration(timedelta=timedelta(days=4, hours=12, seconds=5), monthdelta=monthdelta(3 * 12)))
        self.assertEqual(parsers.duration('P3Y4DT12H30M0.5005S'),
                         duration(timedelta=timedelta(days=4, hours=12, minutes=30,
                          milliseconds=500, microseconds=500), monthdelta=monthdelta(3 * 12)))
        self.assertEqual(parsers.duration('PT.5005S'),
                         duration(timedelta=timedelta(milliseconds=500, microseconds=500), monthdelta=monthdelta(0)))
        self.assertEqual(parsers.duration('P10W'), duration(timedelta=timedelta(weeks=10), monthdelta=monthdelta(0)))
        self.assertEqual(parsers.duration('P7W'), duration(timedelta=timedelta(weeks=7), monthdelta=monthdelta(0)))
        self.assertEqual(parsers.duration('P0003-06-04T12:30:05'),
            duration(timedelta=timedelta(days=4, hours=12, minutes=30, seconds=5), monthdelta=monthdelta(6 + 3 * 12)))
        self.assertEqual(parsers.duration('P00200907T114515'),
            duration(timedelta=timedelta(days=7, hours=11, minutes=45, seconds=15), monthdelta=monthdelta(9 + 20 * 12)))
        self.assertRaises(ValueError, parsers.duration, 'P6Yasdf')
        self.assertRaises(ValueError, parsers.duration, '7432891')
        self.assertRaises(ValueError, parsers.duration, 'asdf')
        self.assertRaises(ValueError, parsers.duration, '23P7DT5H')
        self.assertRaises(ValueError, parsers.duration, '')


if __name__ == '__main__':
    unittest.main()
