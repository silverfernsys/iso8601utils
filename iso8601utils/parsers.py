import calendar
from collections import namedtuple
from monthdelta import MonthDelta as monthdelta
from datetime import datetime as datetime_, timedelta, date as date_, time as time_
from iso8601utils import regex, interval as interval_, duration as duration_
from iso8601utils.tz import TimezoneInfo


Interval = namedtuple('Interval', ['repeat', 'start', 'end', 'delta'])
Duration = namedtuple('Duration', ['timedelta', 'monthdelta'])


def time(time):
    """Parse a string representing an ISO 8601 time and return
    a datetime.time object.
    :param time: A string representing an ISO 8601 time.
    :return: datetime.time
    :raises: ValueError if time is not a valid ISO 8601 time.
    """
    (value, _) = time_24(time)
    return value


def date(date):
    """Parse a string representing an ISO 8601 date and return
    a datetime.date object.
    :param date: A string representing an ISO 8601 date.
    :return: datetime.date
    :raises: ValueError if date is not a valid ISO 8601 date.
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
    """Parse a string representing an ISO 8601 datetime and return
    a datetime.datetime object.
    :param datetime: A string representing an ISO 8601 datetime.
    :return: datetime.datetime
    :raises: ValueError if datetime is not a valid ISO 8601 datetime.
    """
    try:
        return datetime_helper(datetime)
    except Exception as e:
        raise e


def datetime_helper(datetime, allow_missing_time=False):
    try:
        components = datetime.split('T')
        length = len(components)
        if length == 2:
            date_component = components[0]
            time_component = components[1]
            (t, extra_day) = time_24(components[1])
        elif length == 1 and allow_missing_time:
            date_component = [0]
            (t, extra_day) = (time(0), 0)
        else:
            raise ValueError('Invalid ISO 8601 datetime.')

        if extra_day:
            d = date(date_component) + timedelta(days=extra_day)
        else:
            d = date(date_component)
        return datetime_.combine(d, t)
    except:
        raise ValueError('Invalid ISO 8601 datetime.')


def interval(interval, now=datetime_.now(), designator='/'):
    """Parse a string representing an ISO 8601 interval and return
    an iso8601utils.interval object.
    :param interval: A string representing an ISO 8601 interval.
    :return: iso8601utils.interval
    :raises: ValueError if interval is not a valid ISO 8601 interval.
    """
    try:
        components = interval.split(designator)
        return parse_interval(components[1], components[2], parse_repeat(components[0]))
    except Exception as e:
        print('e1: %s' % e)
    try:
        return parse_duration(components[1], now, parse_repeat(components[0]))
    except Exception as e:
        print('e2: %s' % e)
    try:
        return parse_interval(components[0], components[1], 0)
    except Exception as e:
        print('e3: %s' % e)
    try:
        return parse_duration(components[0], now, 0)
    except Exception as e:
        print('e4: %s' % e)

    raise ValueError('Invalid ISO 8601 interval.')


def duration(duration):
    """Parse a string representing an ISO 8601 duration and return
    an iso8601utils.duration object.
    :param duration: A string representing an ISO 8601 duration.
    :return: iso8601utils.duration
    :raises: ValueError if duration is not a valid ISO 8601 duration.
    """
    for r in regex.duration_standard_forms:
        match = r.match(duration)
        if match:
            (t, m) = duration_from_match(match)
            return duration_(timedelta=t, monthdelta=m)

    match = regex.duration_week_form.match(duration)
    if match:
        (t, m) = duration_from_week_from_match(match)
        return duration_(timedelta=t, monthdelta=m)
    raise ValueError('Invalid ISO 8601 duration.')


# Helpers
def parse_repeat(repeat):
    match = regex.repeat.match(repeat)
    if match:
        return float(match.groupdict().get('repeat') or 'inf')
    else:
        raise ValueError('Parsing failed.')


def parse_interval(start, end, repeats):
    try:
        return interval_(start=datetime(start), end=datetime(end), repeats=repeats)
    except Exception as e:
        print('1E: %s' % e)
        raise ValueError('Parsing failed1.')
    try:
        return interval_(start=datetime(start), duration=duration(end), repeats=repeats)
    except Exception as e:
        print('!E: %s' % e)
        raise ValueError('Parsing failed2.')
    try:
        return interval_(end=datetime(end), duration=duration(start), repeats=repeats)
    except Exception as e:
        print('!!E: %s' % e)
        raise ValueError('Parsing failed3.')


def parse_duration(duration_, end, repeats):
    try:
        return interval_(end=end, duration=duration(duration_), repeats=repeats)
    except Exception as e:
        print('pause_duration: %s' % e)
        raise ValueError('Parsing failed4.')


def duration_from_match(match):
    data = {k: float(v or 0.0) for k, v in match.groupdict().items()}
    return (timedelta(days=data['day'],
                     hours=data['hour'],
                     minutes=data['minute'],
                     seconds=data['second']),
            monthdelta(int(data['month'] + 12 * data['year'])))


def duration_from_week_from_match(match):
    return (timedelta(weeks=float(match.groupdict().get('week', 0.0))),
            monthdelta(0))    


def time_24(time):
    """Return a (datetime.time, int) tuple representing the
    ISO 8601 time and the day overflow.
    :param time: A string representing an ISO 8601 time.
    :return: (datetime.time, int)
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

