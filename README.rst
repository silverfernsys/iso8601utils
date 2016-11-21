.. image:: https://img.shields.io/pypi/v/iso8601utils.svg
    :target: https://pypi.python.org/pypi/iso8601utils
.. image:: https://travis-ci.org/silverfernsys/iso8601utils.svg?branch=master
    :target: https://travis-ci.org/silverfernsys/iso8601utils
.. image:: https://codecov.io/gh/silverfernsys/iso8601utils/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/silverfernsys/iso8601utils
.. image:: https://img.shields.io/pypi/l/iso8601utils.svg
    :target: https://pypi.python.org/pypi/iso8601utils
.. image:: https://img.shields.io/pypi/status/iso8601utils.svg
    :target: https://pypi.python.org/pypi/iso8601utils
.. image:: https://img.shields.io/pypi/implementation/iso8601utils.svg
    :target: https://pypi.python.org/pypi/iso8601utils
.. image:: https://img.shields.io/pypi/pyversions/iso8601utils.svg
    :target: https://pypi.python.org/pypi/iso8601utils
.. image:: https://img.shields.io/pypi/format/iso8601utils.svg
    :target: https://pypi.python.org/pypi/iso8601utils
.. image:: https://img.shields.io/librariesio/github/silverfernsys/iso8601utils.svg

iso8601utils
=======================

Datastructures and utilities for representing, parsing, and validating ISO 8601 `dates 
<https://en.wikipedia.org/wiki/ISO_8601#Dates>`_, `times 
<https://en.wikipedia.org/wiki/ISO_8601#Times>`_, `date-times
<https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations>`_, `durations
<https://en.wikipedia.org/wiki/ISO_8601#Durations>`_, and `intervals
<https://en.wikipedia.org/wiki/ISO_8601#Time_intervals>`_.

**Datastructures**

.. code:: python
  
  >>> from iso8601utils import parsers, interval, duration

  # Intervals
  >>> i = parsers.interval('R8/2016-08-01T23:10:59.111Z/2016-08-08T00:13:23.001Z')
  >>> i
  iso8601utils.interval(R8/2016-08-01T23:10:59.111000Z/2016-08-08T00:13:23.001000Z)

  # Decompose interval into an (int, datetime, datetime, iso8601utils.duration)
  # tuple representing (repeats, start, end, duration)
  >>> tuple(i)
  (8, datetime.datetime(2016, 8, 1, 23, 10, 59, 111000, tzinfo=Z), datetime.datetime(2016, 8, 8, 0, 13, 23, 1000, tzinfo=Z), iso8601utils.duration(P6DT1H2M23.89S))
  
  # Public properties
  >>> i.repeats
  8
  >>> i.start
  datetime.datetime(2016, 8, 1, 23, 10, 59, 111000, tzinfo=Z)
  >>> i.end
  datetime.datetime(2016, 8, 8, 0, 13, 23, 1000, tzinfo=Z)
  >>> i.duration
  iso8601utils.duration(P6DT1H2M23.89S)

  # Durations
  >>> d = parsers.duration('P3Y6M4DT12H30M5S')
  >>> d
  iso8601utils.duration(P3Y6M4DT12H30M5S)

  # Decompose duration into a (timedelta, monthdelta) tuple
  >>> tuple(d)
  (datetime.timedelta(4, 45005), MonthDelta(42))
  
  # Public properties
  >>> d.timedelta
  datetime.timedelta(4, 45005)
  >>> d.monthdelta
  MonthDelta(42)

  # Add and subtract durations with datetime objects
  >>> from datetime import datetime
  >>> dt = datetime(2016, 11, 4, 4, 49, 4)
  >>> dt + d
  datetime.datetime(2020, 5, 8, 17, 19, 9)
  >>> dt - d
  datetime.datetime(2013, 4, 30, 16, 18, 59)

  # Add and subtract durations
  >>> a = duration(years=1, months=5, days=3, hours=12)
  >>> b = duration(days=2, hours=5)
  >>> a + b
  iso8601utils.duration(P1Y5M3DT17H)
  >>> a - b
  iso8601utils.duration(P1Y5M1DT7H)

  # Compare durations
  >>> a < b
  False
  >>> a > b
  True

**Parsers**

.. code:: python
  
  >>> from iso8601utils import parsers

  # Parse intervals
  >>> parsers.interval('2016-08-01T23:10:59.111Z/2016-08-08T00:13:23.001Z')
  iso8601utils.interval(2016-08-01T23:10:59.111000Z/2016-08-08T00:13:23.001000Z)

  >>> parsers.interval('R5/2002-08-15T16:20:05.100+08:10/2002-10-12T17:05:25.020-01:40')
  iso8601utils.interval(R5/2002-08-15T16:20:05.100000+08:10/2002-10-12T17:05:25.020000-01:40)

  # Parse durations
  >>> parsers.duration('P3Y6M4DT12H30M5S')
  iso8601utils.duration(P3Y6M4DT12H30M5S)
  
  # Parse times
  >>> parsers.time('13:15+05:10')
  datetime.time(13, 15, tzinfo=+05:10)
  
  # Parse dates
  >>> parsers.date('1981-04-05')
  datetime.date(1981, 4, 5)
  
  # Parse datetimes
  >>> parsers.datetime('2007-08-09T12:30-02:00')
  datetime.datetime(2007, 8, 9, 12, 30, tzinfo=-02:00)
  
  # Parse ordinal dates
  >>> parsers.date('1981-095')
  datetime.date(1981, 4, 5)

  # Parse week dates
  >>> parsers.date('2016-W43-1')
  datetime.date(2016, 10, 24)

**Validators**

.. code:: python

  # Validate strings
  >>> from iso8601utils import validators
  >>> validators.interval('1999-12-31T16:00:00.000+04:00/P5DT7H')
  True
  >>> validators.interval('23P7DT5H')
  False
  >>> validators.duration('P3Y6M4W7DT12H30M5S')
  True
  >>> validators.duration('23P7DT5H')
  False
  >>> validators.time('13:15+05:10')
  True
  >>> validators.date('1981-04-05')
  True
  >>> validators.date('1981-095')
  True
  >>> validators.date('1981-W43-1')
  True
  >>> validators.date('1981W43-1')
  False


