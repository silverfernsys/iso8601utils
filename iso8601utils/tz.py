from copy import deepcopy
from datetime import timedelta, tzinfo


class TimezoneInfo(tzinfo):
    def __init__(self, hours=0, minutes=0, name=None):
        self.offset = timedelta(hours=hours, minutes=minutes)
        self.name = name or self.__class__.__name__

    def __neg__(self):
        neg = deepcopy(self)
        neg.offset = -neg.offset
        return neg

    def __repr__(self):
        total_seconds = self.offset.total_seconds()
        if total_seconds < 0:
            sign = '-'
        else:
            sign = '+'
        hours = int(abs(total_seconds) // 3600)
        minutes = int((abs(total_seconds) % 3600) / 60)
        return '<TimezoneInfo({sign}{hours}:{minutes})>'.format(sign=sign, hours=hours, minutes=minutes)

    def utcoffset(self, dt):
        return self.offset

    def dst(self):
        return timedelta(0)

    def tzname(self):
        return self.name
