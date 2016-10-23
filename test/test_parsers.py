import unittest

try:
    import mock
except:
    from unittest import mock

from monthdelta import MonthDelta as monthdelta
from datetime import datetime as datetime_, timedelta, time as time_, date as date_
from iso8601utils.parsers import interval, duration, time, date, datetime, Interval, Duration
from iso8601utils.tz import TimezoneInfo


class TestParsers(unittest.TestCase):
    def test_time(self):
        with self.assertRaises(ValueError) as context:
            time('1234a')
        self.assertEqual('Malformed ISO 8601 time "1234a".', str(context.exception))
        with self.assertRaises(ValueError) as context:
            time('12:30:40.05+0:15')
        self.assertEqual('Malformed ISO 8601 time "12:30:40.05+0:15".', str(context.exception))
        with self.assertRaises(ValueError) as context:
            time('1230401.05+10:15')
        self.assertEqual('Malformed ISO 8601 time "1230401.05+10:15".', str(context.exception))
        self.assertEqual(time('12'), time_(hour=12))
        self.assertEqual(time('12+05:10'), time_(hour=12, tzinfo=TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(time('12-05:10'), time_(hour=12, tzinfo=-TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(time('13:15'), time_(hour=13, minute=15))
        self.assertEqual(time('13:15+05:10'),
            time_(hour=13, minute=15, tzinfo=TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(time('13:15-05:10'),
            time_(hour=13, minute=15, tzinfo=-TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(time('14:20:50'), time_(hour=14, minute=20, second=50))
        self.assertEqual(time('14:20:50+05:10'),
            time_(hour=14, minute=20, second=50, tzinfo=TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(time('14:20:50-05:10'),
            time_(hour=14, minute=20, second=50, tzinfo=-TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(time('14:20:50+05'),
            time_(hour=14, minute=20, second=50, tzinfo=TimezoneInfo(hours=5)))
        self.assertEqual(time('14:20:50-05'),
            time_(hour=14, minute=20, second=50, tzinfo=-TimezoneInfo(hours=5)))
        self.assertEqual(time('14:20:50+0510'),
            time_(hour=14, minute=20, second=50, tzinfo=TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(time('14:20:50-0510'),
            time_(hour=14, minute=20, second=50, tzinfo=-TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(time('12:30:40.05'), time_(hour=12, minute=30, second=40, microsecond=5))
        self.assertEqual(time('12:30:40.05Z'), time_(hour=12, minute=30, second=40, microsecond=5))
        self.assertEqual(time('12:30:40.05+10:15'),
            time_(hour=12, minute=30, second=40, microsecond=5, tzinfo=TimezoneInfo(hours=10, minutes=15)))
        self.assertEqual(time('12:30:40.05-08:45'),
            time_(hour=12, minute=30, second=40, microsecond=5, tzinfo=-TimezoneInfo(hours=8, minutes=45)))
        self.assertEqual(time('1315'), time_(hour=13, minute=15))
        self.assertEqual(time('1315+05:10'),
            time_(hour=13, minute=15, tzinfo=TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(time('1315-05:10'),
            time_(hour=13, minute=15, tzinfo=-TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(time('142050'), time_(hour=14, minute=20, second=50))
        self.assertEqual(time('142050+05:10'),
            time_(hour=14, minute=20, second=50, tzinfo=TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(time('142050-05:10'),
            time_(hour=14, minute=20, second=50, tzinfo=-TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(time('142050+05'),
            time_(hour=14, minute=20, second=50, tzinfo=TimezoneInfo(hours=5)))
        self.assertEqual(time('142050-05'),
            time_(hour=14, minute=20, second=50, tzinfo=-TimezoneInfo(hours=5)))
        self.assertEqual(time('142050+0510'),
            time_(hour=14, minute=20, second=50, tzinfo=TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(time('142050-0510'),
            time_(hour=14, minute=20, second=50, tzinfo=-TimezoneInfo(hours=5, minutes=10)))
        self.assertEqual(time('123040.05'), time_(hour=12, minute=30, second=40, microsecond=5))
        self.assertEqual(time('123040.05Z'), time_(hour=12, minute=30, second=40, microsecond=5))
        self.assertEqual(time('123040.05+10:15'),
            time_(hour=12, minute=30, second=40, microsecond=5, tzinfo=TimezoneInfo(hours=10, minutes=15)))
        self.assertEqual(time('123040.05-08:45'),
            time_(hour=12, minute=30, second=40, microsecond=5, tzinfo=-TimezoneInfo(hours=8, minutes=45)))


    def test_date(self):
        self.assertEqual(date('1981-095'), date_(1981, 04, 05))
        self.assertEqual(date('1981-04-05'), date_(1981, 04, 05))


    def test_datetime(self):
        self.assertEqual(datetime('2007-04-05T14:30'), datetime_(2007, 4, 5, 14, 30))
        self.assertEqual(datetime('2007-08-09T12:30Z'), datetime_(2007, 8, 9, 12, 30))
        self.assertEqual(datetime('2007-08-09T12:30-02:00'),
            datetime_(2007, 8, 9, 12, 30, tzinfo=-TimezoneInfo(hours=2, minutes=0)))


    def test_interval(self):
        now = datetime_(2016, 1, 1)
        with self.assertRaises(ValueError) as context:
            interval('P6Yasdf')
        self.assertEqual('Malformed ISO 8601 interval "P6Yasdf".', str(context.exception))
        self.assertRaises(ValueError, interval, '7432891')
        self.assertRaises(ValueError, interval, 'asdf')
        self.assertRaises(ValueError, interval, '23P7DT5H')
        self.assertRaises(ValueError, interval, '1999-12-31T16:00:00.000Z')
        self.assertRaises(ValueError, interval, '1999-12-31T16:00:00.000+08:30')
        self.assertRaises(ValueError, interval, 'P6Yasdf/P8Y')
        self.assertRaises(ValueError, interval, 'P7Y/asdf')
        self.assertRaises(ValueError, interval, 'P6Y5M/P9D')
        self.assertRaises(ValueError, interval, '7432891/1234')
        self.assertRaises(ValueError, interval, 'asdf/87rf')
        self.assertRaises(ValueError, interval, '23P7DT5H/89R3')
        self.assertEqual(interval('P7Y', now=now),
                         Interval(0, now - monthdelta(7 * 12), now, (timedelta(0), monthdelta(7 * 12))))
        self.assertEqual(interval('P6W', now=now),
                         Interval(0, now - timedelta(days=6 * 7), now, (timedelta(days=6 * 7), monthdelta(0))))
        self.assertEqual(interval('R1/P6Y5M', now=now),
                         Interval(1, now - monthdelta(6 * 12 + 5), now, (timedelta(0), monthdelta(6 * 12 + 5))))
        self.assertEqual(interval('R5/1999-12-31T16:00:00.000Z/P5DT7H'),
            Interval(5, datetime_(year=1999, month=12, day=31, hour=16),
                datetime_(year=1999, month=12, day=31, hour=16) + timedelta(days=5, hours=7),
                (timedelta(days=5, hours=7), monthdelta(0))))
        self.assertEqual(interval('R7/2016-08-01T23:10:59.111Z/2016-08-08T00:13:23.001Z'),
            Interval(7, datetime_(year=2016, month=8, day=1, hour=23, minute=10, second=59, microsecond=111),
                datetime_(year=2016, month=8, day=8, hour=0, minute=13, second=23, microsecond=1),
                (timedelta(days=6, seconds=3743, microseconds=999890), monthdelta(0))))
        self.assertEqual(interval('R2/P5DT7H/1999-12-31T16:00:00.000Z'),
            Interval(2, datetime_(year=1999, month=12, day=31, hour=16) - timedelta(days=5, hours=7),
                datetime_(year=1999, month=12, day=31, hour=16),
                (timedelta(days=5, seconds=25200), monthdelta(0))))
        self.assertEqual(interval('R5/2002-08-15T16:20:05.100+08:10/P5DT7H'),
            Interval(5, datetime_(year=2002, month=8, day=15, hour=16, minute=20, second=5, microsecond=100,
                    tzinfo=TimezoneInfo(hours=8, minutes=10)),
                datetime_(year=2002, month=8, day=15, hour=16, minute=20, second=5, microsecond=100,
                    tzinfo=TimezoneInfo(hours=8, minutes=10)) + timedelta(days=5, hours=7),
                (timedelta(days=5, hours=7), monthdelta(0))))
        self.assertEqual(interval('2002-08-15T16:20:05.100+08:10/2002-10-12T17:05:25.020-01:40'),
            Interval(0, datetime_(year=2002, month=8, day=15, hour=16, minute=20, second=5, microsecond=100,
                    tzinfo=TimezoneInfo(hours=8, minutes=10)),
                datetime_(year=2002, month=10, day=12, hour=17, minute=5, second=25, microsecond=20,
                    tzinfo=-TimezoneInfo(hours=1, minutes=40)),
                (timedelta(days=-3, seconds=38119, microseconds=999920), monthdelta(2))))
        self.assertEqual(interval('R/P5DT7H/2002-08-15T16:20:05.100+08:10'),
            Interval(float('inf'), datetime_(year=2002, month=8, day=15, hour=16, minute=20, second=5, microsecond=100,
                    tzinfo=TimezoneInfo(hours=8, minutes=10)) - timedelta(days=5, hours=7),
                datetime_(year=2002, month=8, day=15, hour=16, minute=20, second=5, microsecond=100,
                    tzinfo=TimezoneInfo(hours=8, minutes=10)),
                (timedelta(days=5, hours=7), monthdelta(0))))

    def test_duration(self):
        self.assertEqual(duration('P3Y6M4DT12H30M5S'),
                         Duration(timedelta(days=4, hours=12,
                         minutes=30, seconds=5), monthdelta(6 + 3 * 12)))
        self.assertEqual(duration('P6M4DT12H30M15S'),
                         Duration(timedelta(days=4, hours=12,
                          minutes=30, seconds=15), monthdelta(6)))
        self.assertEqual(duration('P6M1DT'),
                         Duration(timedelta(days=1), monthdelta(6)))
        self.assertEqual(duration('P6W'),
                         Duration(timedelta(weeks=6), monthdelta(0)))
        self.assertEqual(duration('P5M3DT5S'),
                         Duration(timedelta(days=3, seconds=5), monthdelta(5)))
        self.assertEqual(duration('P3Y4DT12H5S'),
                         Duration(timedelta(days=4, hours=12, seconds=5), monthdelta(3 * 12)))
        self.assertEqual(duration('P3Y4DT12H30M0.5005S'),
                         Duration(timedelta(days=4, hours=12, minutes=30,
                          milliseconds=500, microseconds=500), monthdelta(3 * 12)))
        self.assertEqual(duration('PT.5005S'),
                         Duration(timedelta(milliseconds=500, microseconds=500), monthdelta(0)))
        self.assertEqual(duration('P10W'), Duration(timedelta(weeks=10), monthdelta(0)))
        self.assertEqual(duration('P7W'), Duration(timedelta(weeks=7), monthdelta(0)))
        self.assertEqual(duration('P0003-06-04T12:30:05'),
            Duration(timedelta(days=4, hours=12, minutes=30, seconds=5), monthdelta(6 + 3 * 12)))
        self.assertEqual(duration('P00200907T114515'),
            Duration(timedelta(days=7, hours=11, minutes=45, seconds=15), monthdelta(9 + 20 * 12)))
        with self.assertRaises(ValueError) as context:
            duration('P6Yasdf')
        self.assertEqual('Malformed ISO 8601 duration "P6Yasdf".', str(context.exception))
        with self.assertRaises(ValueError) as context:
            duration('7432891')
        self.assertEqual('Malformed ISO 8601 duration "7432891".', str(context.exception))
        with self.assertRaises(ValueError) as context:
            duration('asdf')
        self.assertEqual('Malformed ISO 8601 duration "asdf".', str(context.exception))
        with self.assertRaises(ValueError) as context:
            duration('23P7DT5H')
        self.assertEqual('Malformed ISO 8601 duration "23P7DT5H".', str(context.exception))
        with self.assertRaises(ValueError) as context:
            duration('')
        self.assertEqual('Malformed ISO 8601 duration "".', str(context.exception))
