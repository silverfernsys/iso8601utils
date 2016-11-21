import unittest

from datetime import timedelta
from iso8601utils.tz import TimezoneInfo


class TestTimezoneInfo(unittest.TestCase):
    def test_tz(self):
        tz = TimezoneInfo()
        self.assertEqual(tz.offset, timedelta(hours=0, minutes=0))
        self.assertEqual(tz.hours, 0)
        self.assertEqual(tz.minutes, 0)
        self.assertEqual(tuple(tz), (0, 0))
        self.assertEqual(tz.name, tz.tzname(None))
        self.assertEqual(tz.dst(None), timedelta(0))
        self.assertEqual(tz.utcoffset(None), timedelta(0))
        self.assertEqual(tz.__repr__(), '+00:00')
        self.assertEqual(str(tz), '+00:00')

        tz = -TimezoneInfo(hours=5, minutes=20)
        self.assertEqual(tz.hours, -5)
        self.assertEqual(tz.minutes, -20)
        self.assertEqual(tuple(tz), (-5, -20))
        self.assertEqual(tz.name, tz.tzname(None))
        self.assertEqual(tz.dst(None), timedelta(0))
        self.assertEqual(tz.utcoffset(None), -timedelta(hours=5, minutes=20))
        self.assertEqual(tz.__repr__(), '-05:20')
        self.assertEqual(str(tz), '-05:20')

        tz = -TimezoneInfo(hours=4, minutes=30, name='test')
        self.assertEqual(tz.hours, -4)
        self.assertEqual(tz.minutes, -30)
        self.assertEqual(tuple(tz), (-4, -30))
        self.assertEqual(tz.name, 'test')
        self.assertEqual(tz.name, tz.tzname(None))
        self.assertEqual(tz.dst(None), timedelta(0))
        self.assertEqual(tz.utcoffset(None), -timedelta(hours=4, minutes=30))
        self.assertEqual(tz.__repr__(), 'test')
        self.assertEqual(str(tz), 'test')


if __name__ == '__main__':
    unittest.main()