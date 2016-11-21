from collections import namedtuple
from monthdelta import MonthDelta as monthdelta
from datetime import datetime as datetime_, timedelta, date as date_, time as time_
from iso8601utils import regex, match, interval as interval_, duration as duration_
from iso8601utils.tz import TimezoneInfo


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
        match_ = r.match(date)
        if match_:
            return match.date_from_match(match_)
    
    match_ = regex.date_ordinal.match(date)
    if match_:
        return match.ordinal_date_from_match(match_)

    match_ = regex.date_week_0.match(date) or regex.date_week_1.match(date)
    if match_:
        return match.week_date_from_match(match_)

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


def interval(interval, now=datetime_.now(), designator='/'):
    """Parse a string representing an ISO 8601 interval and return
    an iso8601utils.interval object.
    :param interval: A string representing an ISO 8601 interval.
    :return: iso8601utils.interval
    :raises: ValueError if interval is not a valid ISO 8601 interval.
    """
    error_msg = 'Invalid ISO 8601 interval.'
    components = interval.split(designator)
    length = len(components)
    kwargs = {}
    if length == 3:
        try:
            kwargs['repeats'] = repeat(components[0])
        except:
            raise ValueError(error_msg)
        try:
            kwargs['start'] = datetime(components[1])
        except:
            try:
                kwargs['duration'] = duration(components[1])
            except:
                raise ValueError(error_msg)
        try:
            kwargs['end'] = datetime(components[2])
        except:
            try:
                kwargs['duration'] = duration(components[2])
            except:
                raise ValueError(error_msg)
    elif length == 2:
        try:
            kwargs['repeats'] = repeat(components[0])
            kwargs['duration'] = duration(components[1])
            kwargs['end'] = now
        except:
            try:
                kwargs['start'] = datetime(components[0])
                try:
                    kwargs['end'] = datetime(components[1])
                except:
                    try:
                        kwargs['duration'] = duration(components[1])
                    except:
                        raise ValueError(error_msg)
            except:
                try:
                    kwargs['duration'] = duration(components[0])
                    kwargs['end'] = datetime(components[1])
                except:
                    raise ValueError(error_msg)
    elif length == 1:
        try:
            kwargs['duration'] = duration(components[0])
            kwargs['end'] = now
        except:
            raise ValueError(error_msg)
    else:
        raise ValueError(error_msg)

    try:
        return interval_(**kwargs)
    except Exception as e:
        print('E: %s' % e)
        raise ValueError(error_msg)


def duration(duration):
    """Parse a string representing an ISO 8601 duration and return
    an iso8601utils.duration object.
    :param duration: A string representing an ISO 8601 duration.
    :return: iso8601utils.duration
    :raises: ValueError if duration is not a valid ISO 8601 duration.
    """
    for r in regex.duration_standard_forms:
        match_ = r.match(duration)
        if match_:
            (t, m) = match.duration_from_match(match_)
            return duration_(timedelta=t, monthdelta=m)

    match_ = regex.duration_week_form.match(duration)
    if match_:
        (t, m) = match.duration_from_week_from_match(match_)
        return duration_(timedelta=t, monthdelta=m)
    raise ValueError('Invalid ISO 8601 duration.')


def repeat(repeat):
    match_ = regex.repeat.match(repeat)
    if match_:
        return float(match_.groupdict().get('repeat') or 'inf')
    else:
        raise ValueError('Parsing failed.')   


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


def time_24(time):
    """Return a (datetime.time, int) tuple representing the
    ISO 8601 time and the day overflow.
    :param time: A string representing an ISO 8601 time.
    :return: (datetime.time, int)
    """
    try:
        for r in regex.times:
            match_ = r.match(time)
            if match_:
                return match.time_from_match(match_)
    except:
        pass
    raise ValueError('Invalid ISO 8601 time.')
