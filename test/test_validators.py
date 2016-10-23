import unittest

try:
    import mock
except:
    from unittest import mock

from datetime import datetime, timedelta
from iso8601utils.validators import interval, duration


class TestValidators(unittest.TestCase):
    def test_interval(self):
        self.assertTrue(interval('P7Y'))
        self.assertTrue(interval('P6W'))
        self.assertTrue(interval('P6Y5M'))
        self.assertTrue(interval('1999-12-31T16:00:00.000Z/2000-12-31T16:00:00.000+00:30'))
        self.assertTrue(interval('2016-08-01T23:10:59.111-09:30/2016-10-02T12:45:21+04:00'))
        self.assertTrue(interval(
            '1999-12-31T16:00:00.000Z/P5DT7H'))
        self.assertTrue(interval(
            '2016-08-01T23:10:59.111Z/2016-08-08T00:13:23.001Z'))
        self.assertFalse(interval('P6Y5M/P9D'))
        self.assertFalse(interval('P6Yasdf'))
        self.assertFalse(interval('7432891'))
        self.assertFalse(interval('23P7DT5H'))
        self.assertFalse(interval('P6Yasdf/P8Y'))
        self.assertFalse(interval('P7Y/asdf'))
        self.assertFalse(interval('7432891/1234'))
        self.assertFalse(interval('asdf/87rf'))
        self.assertFalse(interval('23P7DT5H/89R3'))

    def test_duration(self):
        self.assertTrue(duration('P3Y6M4DT12H30M5S'))
        self.assertTrue(duration('P6M4DT12H30M15S'))
        self.assertTrue(duration('P6M1DT'))
        self.assertTrue(duration('P6D'))
        self.assertTrue(duration('P5M3DT5S'))
        self.assertTrue(duration('P3Y4DT12H5S'))
        self.assertTrue(duration('P3Y4DT12H30M0.5005S'))
        self.assertTrue(duration('PT.5005S'))
        self.assertFalse(duration('P6Yasdf'))
        self.assertFalse(duration('7432891'))
        self.assertFalse(duration('asdf'))
        self.assertFalse(duration('23P7DT5H'))
        self.assertFalse(duration(''))
