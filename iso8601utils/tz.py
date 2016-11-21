from collections import Iterable
from copy import deepcopy
from datetime import timedelta, tzinfo


class TimezoneInfo(tzinfo, Iterable):
    def __init__(self, hours=0, minutes=0, name=None):
        self.offset = timedelta(hours=hours, minutes=minutes)
        self.name = name or self.string()

    def __neg__(self):
        (hours, minutes) = tuple(self)
        name = self.name if self.name != self.string() else None
        return TimezoneInfo(-hours, -minutes, name)

    @property
    def hours(self):
        total_seconds = self.offset.total_seconds()
        sign = -1 if total_seconds < 0 else 1
        return sign * int(abs(total_seconds) // 3600)

    @property
    def minutes(self):
        total_seconds = self.offset.total_seconds()
        sign = -1 if total_seconds < 0 else 1
        return sign * int((abs(total_seconds) % 3600) / 60)

    def string(self):
        hours, minutes = tuple(self)
        sign = '-' if (hours < 0 or minutes < 0) else '+'
        return '%s%02d:%02d' % (sign, abs(hours), abs(minutes))

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        total_seconds = self.offset.total_seconds()
        sign = -1 if total_seconds < 0 else 1
        yield sign * int(abs(total_seconds) // 3600)
        yield sign * int((abs(total_seconds) % 3600) / 60)

    def utcoffset(self, dt):
        return self.offset

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return self.name


utc = TimezoneInfo(hours=0, minutes=0, name='Z')