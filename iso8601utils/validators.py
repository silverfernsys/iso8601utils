from iso8601utils import regex


def interval(interval):
    """Return a boolean indicating conformance to ISO 8601
    interval specification.
    :param interval: The ISO 8601 interval.
    :return: boolean
    """
    match = regex.interval.match(interval)
    if match:
        return True
    else:
        return False


def duration(duration):
    """Return a boolean indicating conformance to ISO 8601
    duration specification.
    :param duration: The ISO 8601 duration.
    :return: boolean
    """
    match = regex.duration.match(duration)
    if match:
        return True
    else:
        return False
