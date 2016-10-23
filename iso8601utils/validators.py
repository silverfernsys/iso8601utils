from iso8601utils import regex


def time(time):
    """Return a time object representing the ISO 8601 time.
    :param time: The ISO 8601 time.
    :return: boolean
    """
    match = regex.time_form_0.match(time)
    if match:
        return True
    else:
        match = regex.time_form_1.match(time)
        if match:
            return True
        else:   
            raise False


def date(date):
    """Return a date object representing the ISO 8601 date.
    :param date: The ISO 8601 date.
    :return: boolean
    """
    regexes = [regex.date_form_0, regex.date_form_1, regex.date_form_2]
    match = None
    for r in regexes:
        match = r.match(date)
        if match:
            break
    if match:
        return True
    else:
        match = regex.date_ordinal.match(date)
        if match:
            return True
        else:
            return False


def datetime(datetime):
    """Return a datetime object representing the ISO 8601 datetime.
    :param datetime: The ISO 8601 datetime.
    :return: boolean
    """
    try:
        components = datetime.split('T')
        if date(components[0]) and time(components[1]):
            return True
        else:
            return False
    except:
        return False


def interval(interval, designator='/'):
    """Return a pair of datetimes representing start and end datetimes.
    :param interval: The ISO 8601 interval.
    :return: boolean
    """
    components = interval.split(designator)
    if (len(components) == 3 and
        validate_repeat(components[0]) and
        validate_interval(components[1], components[2])):
        return True
    elif (len(components) == 2 and 
            ((components[0][0] == 'R' and validate_repeat(components[0]) and
                duration(components[1])) or
                    validate_interval(components[0], components[1]))):
        return True
    elif (len(components) == 1 and duration(components[0])):
        return True
    else:
        return False


def duration(duration):
    """Return a (timedelta, monthdelta) pair representing duration.
    :param duration: The ISO 8601 duration.
    :return: boolean
    """
    regexes = [regex.duration_form_0, regex.duration_form_1,
        regex.duration_form_2, regex.duration_form_3]
    match = None
    for r in regexes:
        match = r.match(duration)
        if match:
            break
    if match:
        return True
    else:
        return False


# Helpers
def validate_repeat(repeat):
    match = regex.repeat.match(repeat)
    if match:
        return True
    else:
        return False


def validate_interval(start, end):
    if ((datetime(start) and datetime(end)) or 
        (datetime(start) and duration(end)) or
        (duration(start) and datetime(end))):
        return True
    else:
        return False

