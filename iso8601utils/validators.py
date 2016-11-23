from iso8601utils.helpers import regex as r
from iso8601utils.helpers.builder import time_builder


def runner(string, regexes):
    for regex in regexes:
        if regex.match(string):
            return True
    return False


def time(time):
    """Return a time object representing the ISO 8601 time.
    :param time: The ISO 8601 time.
    :return: boolean
    """
    try:
        time_builder(time)
        return True
    except:
        return False


def date(date):
    """Return a date object representing the ISO 8601 date.
    :param date: The ISO 8601 date.
    :return: boolean
    """
    return runner(date, r.dates)


def datetime(datetime):
    """Return a datetime object representing the ISO 8601 datetime.
    :param datetime: The ISO 8601 datetime.
    :return: boolean
    """
    try:
        [date_str, time_str] = datetime.split('T')
        return date(date_str) and time(time_str)
    except:
        return False


def interval(interval, designator='/'):
    """Return a pair of datetimes representing start and end datetimes.
    :param interval: The ISO 8601 interval.
    :return: boolean
    """
    components = interval.split(designator)
    length = len(components)
    if length == 3:
        return validate_repeat(components[0]) and validate_interval(components[1], components[2])
    elif length == 2:
        return ((validate_repeat(components[0]) and duration(components[1])) or
            validate_interval(components[0], components[1]))
    else:
        return duration(components[0])


def duration(duration):
    """Return a (timedelta, monthdelta) pair representing duration.
    :param duration: The ISO 8601 duration.
    :return: boolean
    """
    return runner(duration, r.durations)


# Helpers
def validate_repeat(repeat):
    return r.repeat.match(repeat) != None


def validate_interval(start, end):
    if ((datetime(start) and datetime(end)) or 
        (datetime(start) and duration(end)) or
        (duration(start) and datetime(end))):
        return True
    else:
        return False

