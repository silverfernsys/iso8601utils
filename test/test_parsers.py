import unittest
import mock
from datetime import datetime, timedelta
from iso8601utils.parsers import interval, duration


class TestParsers(unittest.TestCase):
    @mock.patch('iso8601utils.parsers.datetime')
    def test_interval(self, mock_datetime):
        now = datetime(2016, 1, 1)
        mock_datetime.now.return_value = now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)

        with self.assertRaises(ValueError) as context:
            interval('P6Yasdf')
        self.assertIn('Malformed ISO 8601 interval', context.exception.message)
        self.assertEqual(interval('P7Y'),
                         (now - timedelta(days=365 * 7), None))
        self.assertEqual(interval('P6W'),
                         (now - timedelta(days=6 * 7), None))
        self.assertEqual(interval('P6Y5M'),
                         (now - timedelta(days=(365 * 6 + 5 * 30)), None))

        self.assertRaises(
            ValueError, interval, '7432891')
        self.assertRaises(ValueError, interval, 'asdf')
        self.assertRaises(
            ValueError, interval, '23P7DT5H')
        self.assertEqual(
            interval('1999-12-31T16:00:00.000Z'),
            (datetime(year=1999, month=12, day=31, hour=16), None))
        self.assertEqual(
            interval('2016-08-01T23:10:59.111Z'),
            (datetime(year=2016, month=8, day=1, hour=23, minute=10,
                      second=59, microsecond=111), None))

        self.assertRaises(
            ValueError, interval, 'P6Yasdf/P8Y')
        self.assertRaises(
            ValueError, interval, 'P7Y/asdf')
        self.assertEqual(interval('P6Y5M/P9D'),
                         (now - timedelta(days=365 * 6 + 5 * 30),
                          now - timedelta(days=9)))
        self.assertRaises(
            ValueError, interval, '7432891/1234')
        self.assertRaises(
            ValueError, interval, 'asdf/87rf')
        self.assertRaises(
            ValueError, interval, '23P7DT5H/89R3')
        self.assertEqual(
            interval('1999-12-31T16:00:00.000Z/P5DT7H'),
            (datetime(year=1999, month=12, day=31, hour=16),
             now - timedelta(days=5, hours=7)))
        self.assertEqual(
            interval('2016-08-01T23:10:59.111Z/'
                                           '2016-08-08T00:13:23.001Z'),
            (datetime(year=2016, month=8, day=1, hour=23, minute=10,
                      second=59, microsecond=111),
             datetime(year=2016, month=8, day=8, hour=0, minute=13,
                      second=23, microsecond=001)))

    def test_duration(self):
        self.assertEqual(duration('P3Y6M4DT12H30M5S'),
                         timedelta(days=3 * 365 + 6 * 30 + 4,
                                   hours=12, minutes=30, seconds=5))
        self.assertEqual(duration('P6M4DT12H30M15S'),
                         timedelta(days=6 * 30 + 4, hours=12,
                                   minutes=30, seconds=15))
        self.assertEqual(duration('P6M1DT'),
                         timedelta(days=6 * 30 + 1))
        self.assertEqual(duration('P6W'),
                         timedelta(weeks=6))
        self.assertEqual(duration('P5M3DT5S'),
                         timedelta(days=5 * 30 + 3, seconds=5))
        self.assertEqual(duration('P3Y4DT12H5S'),
                         timedelta(days=365 * 3 + 4, hours=12, seconds=5))
        self.assertEqual(duration('P3Y4DT12H30M0.5005S'),
                         timedelta(days=365 * 3 + 4, hours=12, minutes=30,
                                   milliseconds=500, microseconds=500))
        self.assertEqual(duration('PT.5005S'),
                         timedelta(milliseconds=500, microseconds=500))
        self.assertIsNone(duration('P6Yasdf'))
        self.assertIsNone(duration('7432891'))
        self.assertIsNone(duration('asdf'))
        self.assertIsNone(duration('23P7DT5H'))
        self.assertIsNone(duration(''))
