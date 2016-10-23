iso8601utils
=======================

A set of utilities for parsing and validating ISO 8601 `dates 
<https://en.wikipedia.org/wiki/ISO_8601#Dates>`_, `times 
<https://en.wikipedia.org/wiki/ISO_8601#Times>`_, `durations
<https://en.wikipedia.org/wiki/ISO_8601#Durations>`_, and `intervals
<https://en.wikipedia.org/wiki/ISO_8601#Time_intervals>`_ that also
conform to the `rfc3339 <https://tools.ietf.org/html/rfc3339>`_
recommendations.

.. code:: python
  
  >>> from iso8601utils import parsers
  >>> parsers.interval('2016-08-01T23:10:59.111Z/2016-08-08T00:13:23.001Z')
  Interval(repeat=0, start=datetime.datetime(2016, 8, 1, 23, 10, 59, 111),
  end=datetime.datetime(2016, 8, 8, 0, 13, 23, 1),
  delta=(datetime.timedelta(6, 3743, 999890), MonthDelta(0)))

  >>> parsers.interval('2002-08-15T16:20:05.100+08:10/2002-10-12T17:05:25.020-01:40')
  Interval(repeat=0, start=datetime.datetime(2002, 8, 15, 16, 20, 5, 100, tzinfo=<TimezoneInfo(+8:10)>),
  end=datetime.datetime(2002, 10, 12, 17, 5, 25, 20, tzinfo=<TimezoneInfo(-1:40)>),
  delta=(datetime.timedelta(-3, 38119, 999920), MonthDelta(2)))

  >>> parsers.duration('P3Y6M4DT12H30M5S')
  Duration(timedelta=datetime.timedelta(4, 45005), monthdelta=MonthDelta(42))

  >>> from iso8601utils import validators
  >>> validators.interval('1999-12-31T16:00:00.000+04:00/P5DT7H')
  True
  >>> validators.interval('23P7DT5H')
  False
  >>> validators.duration('P3Y6M4W7DT12H30M5S')
  True
  >>> validators.duration('23P7DT5H')
  False

This project does not currently parse week dates.