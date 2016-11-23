from datetime import timedelta, datetime as datetime_
from iso8601utils.helpers import regex as r
from iso8601utils.helpers import match as m


def builder(string, builders):
    for (regex, builder) in builders:
        match = regex.match(string)
        if match:
            return builder(match)
    raise ValueError('Match not found.')


duration_builder = lambda string: builder(string, zip(r.durations,
    [m.duration, m.duration, m.duration, m.duration_week]))


time_builder = lambda string: builder(string, zip(r.times, [m.time, m.time]))


date_builder = lambda string: builder(string, zip(r.dates,
    [m.date, m.date, m.date, m.date_week, m.date_week, m.date_ordinal]))


def datetime_builder(string):
    try:
        [date, time] = string.split('T')
        (t, extra_day) = time_builder(time)
        d = date_builder(date) + timedelta(days=extra_day)
        return datetime_.combine(d, t)
    except:
        raise ValueError('Parsing failed.')


def repeat_builder(repeat):
    try:
        value = r.repeat.match(repeat).groupdict().get('repeat')
        return int(value) if value else float('inf')
    except:
        raise ValueError('Parsing failed.')