import calendar
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
    (value, _) = time_24(time)
    return value


def date(date):
    """Return a date object representing the ISO 8601 date.
    :param date: The ISO 8601 date.
    :return: date
    """
    for r in regex.date_calendars:
        match = r.match(date)
        if match:
            return date_from_match(match)
    
    match = regex.date_ordinal.match(date)
    if match:
        return ordinal_date_from_match(match)

    match = regex.date_week_0.match(date) or regex.date_week_1.match(date)
    if match:
        return week_date_from_match(match)

    raise ValueError('Invalid ISO 8601 date.')


def datetime(datetime):
    """Return a datetime object representing the ISO 8601 datetime.
    :param datetime: The ISO 8601 datetime.
    :return: datetime
    """
    try:
        components = datetime.split('T')
        (t, extra_day) = time_24(components[1])
        if extra_day:
            d = date(components[0]) + timedelta(days=extra_day)
        else:
            d = date(components[0])
        return datetime_.combine(d, t)
    except:
        raise ValueError('Invalid ISO 8601 datetime.')


def interval(interval, now=datetime_.now(), designator='/'):
    """Return a named tuple representing repeat,
    start and end datetimes, and duration.
    :param interval: The ISO 8601 interval.
    :return: Interval(float, datetime, datetime, Duration(timedelta, monthdelta))
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
        raise ValueError('Invalid ISO 8601 interval.')


def duration(duration):
    """Return a named tuple representing duration.
    :param duration: The ISO 8601 duration.
    :return: Duration(timedelta, monthdelta)
    """
    for r in regex.duration_standard_forms:
        match = r.match(duration)
        if match:
            (t, m) = duration_from_match(match)
            return Duration(t, m)

    match = regex.duration_week_form.match(duration)
    if match:
        (t, m) = duration_from_week_form_match(match)
        return Duration(t, m)
    raise ValueError('Invalid ISO 8601 duration.')


# Helpers
def parse_repeat(repeat):
    match = regex.repeat.match(repeat)
    if match:
        return float(match.groupdict().get('repeat') or 'inf')
    else:
        raise ValueError('Parsing failed.')


def parse_interval(start, end):
    s = e = delta = None
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
    except:
        raise ValueError('Parsing failed.')


def duration_from_match(match):
    data = {k: float(v or 0.0) for k, v in match.groupdict().items()}
    return (timedelta(days=data['day'],
                     hours=data['hour'],
                     minutes=data['minute'],
                     seconds=data['second']),
            monthdelta(int(data['month'] + 12 * data['year'])))


def duration_from_week_form_match(match):
    return (timedelta(weeks=float(match.groupdict().get('week', 0.0))),
            monthdelta(0))    


def time_24(time):
    """Return a time object representing the ISO 8601 time.
    :param time: The ISO 8601 time.
    :return: time
    """
    try:
        for r in regex.times:
            match = r.match(time)
            if match:
                return time_from_match(match)
    except:
        pass
    raise ValueError('Invalid ISO 8601 time.')


def time_from_match(match):
    group = match.groupdict()
    data = {k: int(v or 0) for k, v in group.items() if k != 'sign'}
    sign = group.get('sign')
    if sign:
        hours = data['offset_hour']
        minutes = data['offset_minute']
        if hours == minutes == 0:
            raise ValueError('Invalid timezone offset {0}00:00.'.format(sign))

        if sign == '+':
            tz = TimezoneInfo(hours=hours, minutes=minutes)
        else:
            tz = -TimezoneInfo(hours=hours, minutes=minutes)
    else:
        tz = None

    hour, minute = data['hour'], data['minute']
    second, microsecond = data['second'], data['microsecond']
    day = 0
    if hour == 24 and minute == second == microsecond == 0:
        hour = 0
        day = 1

    return (time_(hour, minute, second, microsecond, tz), day)


def date_from_match(match):
    data = {k: int(v) for k, v in match.groupdict().items() if v}
    return date_(data.get('year', 1), data.get('month', 1), data.get('day', 1))


def ordinal_date_from_match(match):
    data = {k: int(v) for k, v in match.groupdict().items() if v}
    days = (date_(data.get('year', 1), 1, 1) - date_(1, 1, 1)).days
    return date_.fromordinal(days + data.get('day', 0))


def days_in_year(year):
    if calendar.isleap(int(year)):
        return 366
    else:
        return 365


def week_date_from_match(match):
    data = {k: int(v or 1) for k, v in match.groupdict().items()}
    year = data['year']
    week = data['week']
    day = data['day']

    ordinal = week * 7 + day - ((date_(year, 1, 4).weekday() + 1) + 3)
    if ordinal < 1:
        ordinal += days_in_year(year - 1)
        year -= 1
    elif ordinal > days_in_year(year):
        ordinal -= days_in_year(year)
        year += 1

    return date_(year, 1, 1) + timedelta(days=(ordinal - 1))

