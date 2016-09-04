import regex


def interval(interval):
    match = regex.interval.match(interval)
    if match:
        return True
    else:
        return False


def duration(duration):
    match = regex.duration.match(duration)
    if match:
        return True
    else:
        return False