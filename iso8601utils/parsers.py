from collections import namedtuple
from monthdelta import MonthDelta as monthdelta
from datetime import datetime as datetime_, timedelta, date as date_, time as time_
from iso8601utils import regex
from iso8601utils.tz import TimezoneInfo


Interval = namedtuple('Interval', ['repeat', 'start', 'end', 'delta'])
Duration = namedtuple('Duration', ['timedelta', 'monthdelta'])


def time(time):
    """Return a time object representing the ISO 8601 time.
    :param time: The ISO 8601 time.
    :return: time
    """
    match = regex.time_form_0.match(time)
    if match:
        return time_from_dict(match.groupdict())
    else:
        match = regex.time_form_1.match(time)
        if match:
            return time_from_dict(match.groupdict())
        else:   
            raise ValueError('Malformed ISO 8601 time "{0}".'.
                             format(time))


def date(date):
    """Return a date object representing the ISO 8601 date.
    :param date: The ISO 8601 date.
    :return: date
    """
    regexes = [regex.date_form_0, regex.date_form_1, regex.date_form_2]
    match = None
    for r in regexes:
        match = r.match(date)
        if match:
            break
    if match:
        return date_from_dict(match.groupdict())
    else:
        match = regex.date_ordinal.match(date)
        if match:
            return ordinal_date_from_dict(match.groupdict())
        else:
            raise ValueError('Malformed ISO 8601 date "{0}".'.
                             format(date))


def datetime(datetime):
    """Return a datetime object representing the ISO 8601 datetime.
    :param datetime: The ISO 8601 datetime.
    :return: datetime
    """
    try:
        components = datetime.split('T')
        d = date(components[0])
        t = time(components[1])
        return datetime_.combine(d, t)
    except:
        raise ValueError('Malformed ISO 8601 datetime "{0}".'.
                         format(datetime))


def interval(interval, now=datetime_.now(), designator='/'):
    """Return a pair of datetimes representing start and end datetimes.
    :param interval: The ISO 8601 interval.
    :return: Interval(float, datetime, datetime, (timedelta, monthdelta))
    """
    try:
        components = interval.split(designator)
        if len(components) == 3:
            repeat = parse_repeat(components[0])
            (start, end, duration) = parse_interval(components[1], components[2])
        elif len(components) == 2:
            if components[0][0] == 'R':
                repeat = parse_repeat(components[0])
                end = now
                (start, duration) = parse_duration(components[1], end)
            else:
                repeat = 0
                (start, end, duration) = parse_interval(components[0], components[1])
        else:
            repeat = 0
            end = now
            (start, duration) = parse_duration(components[0], end)
        return Interval(repeat, start, end, duration)
    except:
        raise ValueError('Malformed ISO 8601 interval "{0}".'.
                         format(interval))


def duration(duration):
    """Return a (timedelta, monthdelta) pair representing duration.
    :param duration: The ISO 8601 duration.
    :return: Duration(timedelta, monthdelta)
    """
    regexes = [regex.duration_form_0, regex.duration_form_1,
        regex.duration_form_2, regex.duration_form_3]
    match = None
    for r in regexes:
        match = r.match(duration)
        if match:
            break
    if match:
        (t, m) = duration_from_dict(match.groupdict())
        return Duration(t, m)
    else:
        raise ValueError('Malformed ISO 8601 duration "{0}".'.
                         format(duration))


# Helpers
def parse_repeat(repeat):
    match = regex.repeat.match(repeat)
    if match:
        return float(match.groupdict().get('repeat') or 'inf')
    else:
        raise ValueError('Parsing failed.')


def parse_interval(start, end):
    # Parse explicit form
    try:
        s = datetime(start)
        e = datetime(end)
        delta = (e.replace(month=s.month, year=s.year) - s,
            monthdelta((e.month - s.month) + 12 * (e.year - s.year)))
    except:
        pass

    # Parse start form
    try:
        s = datetime(start)
        delta = duration(end)
        e = s + delta[0] + delta[1]
    except:
        pass

    # Parse end form
    try:
        delta = duration(start)
        e = datetime(end)
        s = e - delta[0] - delta[1]
    except:
        pass

    if s and e and delta:
        return (s, e, delta)
    else:
        raise ValueError('Parsing failed.')


def parse_duration(duration_, end):
    try:
        delta = duration(duration_)
        start = end - delta[0] - delta[1]
        return (start, delta)
    except Exception as e:
        raise ValueError('Parsing failed.')


def duration_from_dict(dict):
    data = {k: float(v) for k, v in dict.items() if v}
    return (timedelta(weeks=data.get('week', 0.0),
                     days=data.get('day', 0.0),
                     hours=data.get('hour', 0.0),
                     minutes=data.get('minute', 0.0),
                     seconds=data.get('second', 0.0)),
            monthdelta(int(data.get('month', 0.0) + 12 * data.get('year', 0.0))))


def time_from_dict(dict):
    data = {k: int(v) for k, v in dict.items() if v and k != 'sign'}
    sign = dict.get('sign')
    if sign:
        if sign is '+':
            tz = TimezoneInfo(hours=data.get('offset_hour', 0),
                minutes=data.get('offset_minute', 0))
        else:
            tz = -TimezoneInfo(hours=data.get('offset_hour', 0),
                minutes=data.get('offset_minute', 0))
    else:
        tz = None

    return time_(hour=data.get('hour', 0),
                 minute=data.get('minute', 0),
                 second=data.get('second', 0),
                 microsecond=data.get('microsecond', 0),
                 tzinfo=tz)


def date_from_dict(dict):
    data = {k: int(v) for k, v in dict.items() if v}
    return date_(data.get('year', 1), data.get('month', 1), data.get('day', 1))


def ordinal_date_from_dict(dict):
    data = {k: int(v) for k, v in dict.items() if v}
    days = (date_(data.get('year', 1), 1, 1) - date_(1, 1, 1)).days
    return date_.fromordinal(days + data.get('day', 0))
