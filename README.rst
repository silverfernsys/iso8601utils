iso8601utils
=======================

A set of utilities for parsing and validating iso8601 `durations
<https://en.wikipedia.org/wiki/ISO_8601#Durations>`_ and `intervals
<https://en.wikipedia.org/wiki/ISO_8601#Time_intervals`_.

.. code:: python

  from iso8601utils import parsers
  parsers.interval()
  (start, end)

  parsers.duration()
  (duration)

  from iso8601utils import validators
  validators.interval()
  True
  validators.interval()
  False
  validators.duration()
  True
  validators.duration()
  False

This project currently only supports utc times.