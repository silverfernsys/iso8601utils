import pytest


from datetime import datetime, timedelta
from iso8601utils.validators import interval, duration, date, time, datetime


def test_interval():
    assert interval('P7Y') == True
    assert interval('P6W') == True
    assert interval('P6Y5M') == True
    assert interval('1999-12-31T16:00:00.000Z/2000-12-31T16:00:00.000+00:30') == True
    assert interval('2016-08-01T23:10:59.111-09:30/2016-10-02T12:45:21+04:00') == True
    assert interval('1999-12-31T16:00:00.000Z/P5DT7H') == True
    assert interval('R5/2016-08-01T23:10:59.111Z/2016-08-08T00:13:23.001Z') == True
    assert interval('P6Y5M/P9D') == False
    assert interval('P6Yasdf') == False
    assert interval('7432891') == False
    assert interval('23P7DT5H') == False
    assert interval('P6Yasdf/P8Y') == False
    assert interval('P7Y/asdf') == False
    assert interval('7432891/1234') == False
    assert interval('asdf/87rf') == False
    assert interval('23P7DT5H/89R3') == False
    assert interval('T5/2016-08-01T23:10:59.111Z/2016-08-08T00:13:23.001Z') == False


def test_duration():
    assert duration('P3Y6M4DT12H30M5S') == True
    assert duration('P6M4DT12H30M15S') == True
    assert duration('P6M1DT') == True
    assert duration('P6D') == True
    assert duration('P5M3DT5S') == True
    assert duration('P3Y4DT12H5S') == True
    assert duration('P3Y4DT12H30M0.5005S') == True
    assert duration('PT.5005S') == True
    assert duration('P6Yasdf') == False
    assert duration('7432891') == False
    assert duration('asdf') == False
    assert duration('23P7DT5H') == False
    assert duration('') == False


def test_date():
    assert date('2008-W39-6') == True
    assert date('2008W396') == True
    assert date('2016W431') == True
    assert date('2016-W43-1') == True
    assert date('1981-095') == True
    assert date('1981095') == True
    assert date('1981-04-05') == True
    assert date('19810405') == True
    assert date('--04-03') == True
    assert date('--1001') == True
    assert date('2008-W396') == False
    assert date('2008W39-6') == False
    assert date('198195') == False
    assert date('1981-0405') == False
    assert date('198104-05') == False

def test_time():
    assert time('1234a') == False
    assert time('12:30:40.05+0:15') == False
    assert time('1230401.05+10:15') == False
    assert time('24:00:00.0001') == False
    assert time('12') == True
    assert time('24:00:00') == True
    assert time('00:00:00') == True
    assert time('12+05:10') == True
    assert time('12-05:10') == True
    assert time('13:15') == True
    assert time('13:15+05:10') == True
    assert time('13:15-05:10') == True
    assert time('14:20:50') == True
    assert time('14:20:50+05:10') == True
    assert time('14:20:50-05:10') == True
    assert time('14:20:50+05') == True
    assert time('14:20:50-05') == True
    assert time('14:20:50+0510') == True
    assert time('14:20:50-0510') == True
    assert time('12:30:40.05') == True
    assert time('12:30:40.05Z') == True
    assert time('12:30:40.05+10:15') == True
    assert time('12:30:40.05-08:45') == True
    assert time('1315') == True
    assert time('1315+05:10') == True
    assert time('1315-05:10') == True
    assert time('142050') == True
    assert time('142050+05:10') == True
    assert time('142050-05:10') == True
    assert time('142050+05') == True
    assert time('142050-05') == True
    assert time('142050+0510') == True
    assert time('142050-0510') == True
    assert time('123040.05') == True
    assert time('123040.05Z') == True
    assert time('123040.05+10:15') == True
    assert time('123040.05-08:45') == True


def test_datetime():
    assert datetime('2007-04-05T14:30') == True
    assert datetime('2007-08-09T12:30Z') == True
    assert datetime('2007-01-01T24:00:00') == True
    assert datetime('2007-01-02T00:00:00') == True
    assert datetime('2007-08-09T12:30-02:00') == True
    assert datetime('007-04-15T12:30') == False
    assert datetime('2007-08-09T12:30+0') == False
    assert datetime('2007-08-09T12:30-02:aa') == False
