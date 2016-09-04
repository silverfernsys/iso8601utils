iso8601utils
=======================

A set of utilities for parsing and validating iso8601 `durations
<https://en.wikipedia.org/wiki/ISO_8601#Durations>`_ and `intervals
<https://en.wikipedia.org/wiki/ISO_8601#Time_intervals>`_.

.. code:: python

  from iso8601utils import parsers
  parsers.interval('2016-08-01T23:10:59.111Z/2016-08-08T00:13:23.001Z')
  (datetime.datetime(2016, 8, 1, 23, 10, 59, 111), datetime.datetime(2016, 8, 8, 0, 13, 23, 1))

  parsers.duration('P3Y6M4DT12H30M5S')
  datetime.timedelta(1279, 45005)

  from iso8601utils import validators
  validators.interval('1999-12-31T16:00:00.000Z/P5DT7H')
  True
  validators.interval('23P7DT5H')
  False
  validators.duration('P3Y6M4W7DT12H30M5S')
  True
  validators.duration('23P7DT5H')
  False

This project currently only supports utc times.