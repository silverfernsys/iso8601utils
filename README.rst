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
  delta=Duration(timedelta=datetime.timedelta(6, 3743, 999890), monthdelta=MonthDelta(0)))

  >>> parsers.interval('2002-08-15T16:20:05.100+08:10/2002-10-12T17:05:25.020-01:40')
  Interval(repeat=0, start=datetime.datetime(2002, 8, 15, 16, 20, 5, 100, tzinfo=<TimezoneInfo(+8:10)>),
  end=datetime.datetime(2002, 10, 12, 17, 5, 25, 20, tzinfo=<TimezoneInfo(-1:40)>),
  delta=Duration(timedelta=datetime.timedelta(-3, 38119, 999920), monthdelta=MonthDelta(2)))

  >>> parsers.duration('P3Y6M4DT12H30M5S')
  Duration(timedelta=datetime.timedelta(4, 45005), monthdelta=MonthDelta(42))

  >>> parsers.time('13:15+05:10')
  datetime.time(13, 15, tzinfo=<TimezoneInfo(+5:10)>)

  >>> parsers.date('1981-04-05')
  datetime.date(1981, 4, 5)

  >>> parsers.datetime('2007-08-09T12:30-02:00')
  datetime.datetime(2007, 8, 9, 12, 30, tzinfo=<TimezoneInfo(-2:0)>)

  >>> parsers.date('1981-095')
  datetime.date(1981, 4, 5)

  >>> parsers.date('2016-W43-1')
  datetime.date(2016, 10, 24)

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


