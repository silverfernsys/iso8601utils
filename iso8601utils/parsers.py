from datetime import datetime as datetime_
from iso8601utils import interval as interval_
from iso8601utils.helpers.builder import (duration_builder, time_builder, date_builder,
    datetime_builder, repeat_builder)


def time(time):
    """Parse a string representing an ISO 8601 time and return
    a datetime.time object.
    :param time: A string representing an ISO 8601 time.
    :return: datetime.time
    :raises: ValueError if time is not a valid ISO 8601 time.
    """
    try:
        return time_builder(time)[0]
    except:
        raise ValueError('Invalid ISO 8601 time.')


def date(date):
    """Parse a string representing an ISO 8601 date and return
    a datetime.date object.
    :param date: A string representing an ISO 8601 date.
    :return: datetime.date
    :raises: ValueError if date is not a valid ISO 8601 date.
    """
    try:
        return date_builder(date)
    except:
        raise ValueError('Invalid ISO 8601 date.')


def datetime(datetime):
    """Parse a string representing an ISO 8601 datetime and return
    a datetime.datetime object.
    :param datetime: A string representing an ISO 8601 datetime.
    :return: datetime.datetime
    :raises: ValueError if datetime is not a valid ISO 8601 datetime.
    """
    try:
        return datetime_builder(datetime)
    except Exception as e:
        raise ValueError('Invalid ISO 8601 datetime.')


def duration(duration):
    """Parse a string representing an ISO 8601 duration and return
    an iso8601utils.duration object.
    :param duration: A string representing an ISO 8601 duration.
    :return: iso8601utils.duration
    :raises: ValueError if duration is not a valid ISO 8601 duration.
    """
    try:
        return duration_builder(duration)
    except:
        raise ValueError('Invalid ISO 8601 duration.')


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
            kwargs['repeats'] = repeat_builder(components[0])
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
            kwargs['repeats'] = repeat_builder(components[0])
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
    except:
        raise ValueError(error_msg) 
