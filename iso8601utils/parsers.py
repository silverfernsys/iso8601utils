from monthdelta import MonthDelta as monthdelta
from datetime import datetime, timedelta
from iso8601utils import regex


def interval(interval):
    """Return a pair of datetimes representing start and end datetimes.
    :param interval: The ISO 8601 interval.
    :return: (datetime, datetime)
    """
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

        now = datetime.now()
        if len(s_i.keys()) > 0 and len(s_dt.keys()) == 0:
            (time, month) = deltas_from_dict(s_i, 's_i_')
            start = now - time - month
        elif len(s_i.keys()) == 0 and len(s_dt.keys()) > 0:
            start = datetime_from_dict(s_dt, 's_dt_')
        else:
            raise ValueError('Malformed ISO 8601 interval "{0}".'.
                             format(interval))

        if len(e_i.keys()) > 0 and len(e_dt.keys()) == 0:
            (time, month) = deltas_from_dict(e_i, 'e_i_')
            end = now - time - month
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
    """Return a (timedelta, monthdelta) pair representing duration.
    :param duration: The ISO 8601 duration.
    :return: (timedelta, monthdelta)
    """
    match = regex.duration.match(duration)
    if match:
        items = match.groupdict().items()
        return deltas_from_dict({k: float(v) for k, v in items if v})
    else:
        return (None, None)


def deltas_from_dict(dict, prefix=''):
    return (timedelta(weeks=dict.get(prefix + 'week', 0.0),
                     days=dict.get(prefix + 'day', 0.0)
                     + 365 * dict.get(prefix + 'year', 0.0),
                     hours=dict.get(prefix + 'hour', 0.0),
                     minutes=dict.get(prefix + 'minute', 0.0),
                     seconds=dict.get(prefix + 'second', 0.0)),
            monthdelta(int(dict.get(prefix + 'month', 0.0))))


def datetime_from_dict(dict, prefix=''):
    return datetime(year=dict.get(prefix + 'year', 0),
                    month=dict.get(prefix + 'month', 0),
                    day=dict.get(prefix + 'day', 0),
                    hour=dict.get(prefix + 'hour', 0),
                    minute=dict.get(prefix + 'minute', 0),
                    second=dict.get(prefix + 'second', 0),
                    microsecond=dict.get(prefix + 'microsecond', 0))
