from calendar import isleap
from datetime import timedelta, date as date_, time as time_
from monthdelta import MonthDelta as monthdelta
from iso8601utils.tz import TimezoneInfo, utc


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
        tz = utc

    hour, minute = data['hour'], data['minute']
    second, millisecond = data['second'], data['millisecond']
    day = 0
    if hour == 24 and minute == second == millisecond == 0:
        hour = 0
        day = 1

    return (time_(hour, minute, second, 1000 * millisecond, tz), day)


def date_from_match(match):
    data = {k: int(v) for k, v in match.groupdict().items() if v}
    return date_(data.get('year', 1), data.get('month', 1), data.get('day', 1))


def ordinal_date_from_match(match):
    data = {k: int(v) for k, v in match.groupdict().items() if v}
    days = (date_(data.get('year', 1), 1, 1) - date_(1, 1, 1)).days
    return date_.fromordinal(days + data.get('day', 0))


def days_in_year(year):
    return 366 if isleap(int(year)) else 365


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
