from iso8601utils import regex
from iso8601utils.parsers import time_24

def time(time):
    """Return a time object representing the ISO 8601 time.
    :param time: The ISO 8601 time.
    :return: boolean
    """
    try:
        time_24(time)
        return True
    except:
        return False


def date(date):
    """Return a date object representing the ISO 8601 date.
    :param date: The ISO 8601 date.
    :return: boolean
    """
    for r in regex.date_calendars + [regex.date_ordinal,
        regex.date_week_0, regex.date_week_1]:
        if r.match(date):
            return True
    return False


def datetime(datetime):
    """Return a datetime object representing the ISO 8601 datetime.
    :param datetime: The ISO 8601 datetime.
    :return: boolean
    """
    try:
        components = datetime.split('T')
        return date(components[0]) and time(components[1])
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
    for r in [regex.duration_form_0, regex.duration_form_1,
        regex.duration_form_2, regex.duration_week_form]:
        if r.match(duration):
            return True
    return False


# Helpers
def validate_repeat(repeat):
    return regex.repeat.match(repeat) != None


def validate_interval(start, end):
    if ((datetime(start) and datetime(end)) or 
        (datetime(start) and duration(end)) or
        (duration(start) and datetime(end))):
        return True
    else:
        return False

