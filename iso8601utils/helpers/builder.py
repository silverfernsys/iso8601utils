from datetime import timedelta, datetime as datetime_, time as time_
from iso8601utils.helpers import regex as r
from iso8601utils.helpers import match as m
from iso8601utils.tz import utc


def builder(string, builders):
    for (regex, builder) in builders:
        match = regex.match(string)
        if match:
            return builder(match)
    raise ValueError('Match not found.')


def partial_builder(string, builders, other=None):
    for (regex, builder) in builders:
        match = regex.match(string)
        if match:
            return builder(match, other)
    raise ValueError('Match not found.')


duration_builder = lambda string: builder(string, zip(r.durations,
    [m.duration, m.duration, m.duration_week]))


time_builder = lambda string: builder(string, [(r.time, m.time)])


date_builder = lambda string: builder(string, zip(r.dates,
    [m.date, m.date, m.date_week, m.date_ordinal]))


date_builder_strict = lambda string, other=None: builder(string, zip(r.dates_strict,
    [m.date, m.date, m.date_week, m.date_ordinal]))

date_builder_partial = lambda string, other=None: partial_builder(string, zip(r.dates_partial,
    [m.date, m.date]), other)


def datetime_builder(string):
    try:
        [date, time] = string.split('T')
        (t, extra_day, _) = time_builder(time)
        d = date_builder(date) + timedelta(days=extra_day)
        return datetime_.combine(d, t)
    except Exception as e:
        raise ValueError('Parsing failed.')


def datetime_builder_partial(string, delta=None, other=None, strict=False):
    def resolve_tz(value, other, explicit=True):
        """If end does not have a tzinfo attribute, but
        start does, modify end to have a tzinfo attribute.
        """
        if (not explicit or value.tzinfo == None) and (other and other.tzinfo != None):
            return value.replace(tzinfo=other.tzinfo)
        return value

    # select builder
    if strict:
        selected_builder = date_builder_strict
    else:
        selected_builder = date_builder_partial

    # date and time components
    components = string.split('T')
    length = len(components)
    if length == 2:
        try:
            [date, time] = components
            (t, extra_day, explicit_tz) = time_builder(time)
            print('EXPLICIT: %s' % explicit_tz)
            t = resolve_tz(t, other, explicit_tz)
            d = selected_builder(date, other) + timedelta(days=extra_day)
            return datetime_.combine(d, t)
        except:
            raise ValueError('Parsing failed.')
    elif length == 1:
        # only date component
        try:
            if delta:
                d = selected_builder(string, other) + delta
            else:
                d = selected_builder(string, other)
            return resolve_tz(datetime_.combine(d, time_(0, tzinfo=utc)), other)
        # only time component
        except:
            try:
                (t, extra_day, explicit_tz) = time_builder(string)
                t = resolve_tz(t, other, explicit_tz)
                return datetime_.combine(other.date(), t)
            except:
                raise ValueError('Parsing failed.')
    else:
        raise ValueError('Parsing failed.')


def interval_datetimes_builder(start, end):
    """Build a datetime from a partial representation filling
    in missing values with values from other. Need to keep track
    of possible extra_day returned from time_builder(start)
    """
    try:
        s = datetime_builder_partial(start, strict=True)
        e = datetime_builder_partial(end, timedelta(1), s)
        if e > s:
            return (s, e)
        else:
            raise ValueError('Parsing failed: end < start.')
    except:
        raise ValueError('Parsing failed.')


def repeat_builder(repeat):
    try:
        value = r.repeat.match(repeat).groupdict().get('repeat')
        return int(value) if value else float('inf')
    except:
        raise ValueError('Parsing failed.')
