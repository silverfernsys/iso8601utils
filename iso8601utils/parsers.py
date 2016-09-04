from datetime import datetime, timedelta
import regex


def interval(interval):
    match = regex.interval.match(interval)
    if match:
        s_i = {k: float(v) for k, v in match.groupdict().items()
               if v and k.startswith('s_i_')}
        s_dt = {k: int(v) for k, v in match.groupdict().items()
                if v and k.startswith('s_dt_')}
        e_i = {k: float(v) for k, v in match.groupdict().items()
               if v and k.startswith('e_i_')}
        e_dt = {k: int(v) for k, v in match.groupdict().items()
                if v and k.startswith('e_dt_')}

        if len(s_i.keys()) > 0 and len(s_dt.keys()) == 0:
            start = datetime.now() - timedelta_from_dict(s_i, 's_i_')
        elif len(s_i.keys()) == 0 and len(s_dt.keys()) > 0:
            start = datetime_from_dict(s_dt, 's_dt_')
        else:
            raise ValueError('Malformed ISO 8601 interval "{0}".'.
                             format(interval))

        if len(e_i.keys()) > 0 and len(e_dt.keys()) == 0:
            end = datetime.now() - timedelta_from_dict(e_i, 'e_i_')
        elif len(e_i.keys()) == 0 and len(e_dt.keys()) > 0:
            end = datetime_from_dict(e_dt, 'e_dt_')
        elif len(e_i.keys()) == 0 and len(e_dt.keys()) == 0:
            end = None
        else:
            raise ValueError('Malformed ISO 8601 interval "{0}".'.
                             format(interval))
        return (start, end)
    else:
        raise ValueError('Malformed ISO 8601 interval "{0}".'.
                         format(interval))


def duration(duration):
    """ Extracts a string such as P3Y6M4DT12H30M5S to
    a timedelta object.
    NOTE: Months are converted into 30 days.
    NOTE: Years are converted into 365 days.
    """
    match = regex.duration.match(duration)
    if match:
        items = match.groupdict().items()
        return timedelta_from_dict({k: float(v)
                                    for k, v in items if v})
    else:
        return None


def timedelta_from_dict(dict, prefix=''):
    return timedelta(weeks=dict.get(prefix + 'week', 0.0),
                     days=dict.get(prefix + 'day', 0.0)
                     + 30 * dict.get(prefix + 'month', 0.0)
                     + 365 * dict.get(prefix + 'year', 0.0),
                     hours=dict.get(prefix + 'hour', 0.0),
                     minutes=dict.get(prefix + 'minute', 0.0),
                     seconds=dict.get(prefix + 'second', 0.0))


def datetime_from_dict(dict, prefix=''):
    return datetime(year=dict.get(prefix + 'year', 0),
                    month=dict.get(prefix + 'month', 0),
                    day=dict.get(prefix + 'day', 0),
                    hour=dict.get(prefix + 'hour', 0),
                    minute=dict.get(prefix + 'minute', 0),
                    second=dict.get(prefix + 'second', 0),
                    microsecond=dict.get(prefix + 'microsecond', 0))
