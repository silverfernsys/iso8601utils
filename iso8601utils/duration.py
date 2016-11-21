from collections import Iterable
from datetime import datetime, timedelta
from enum import Enum
from monthdelta import MonthDelta as monthdelta

try:
    from itertools import izip as zip
except:
    pass


class duration(Iterable):
    Format = Enum('Format', 'DURATION BASIC EXTENDED WEEK')

    def __init__(self, *args, **kwargs):
        def resolve_args(args, kwargs):
            keys = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
            for k, v in zip(keys, args):
                if k in kwargs:
                    raise ValueError('\'%s\' already provided as a positional argument.' % k)
                kwargs[k] = v
            return kwargs

        def create_deltas(years=0, months=0, days=0, hours=0, minutes=0, seconds=0):
            td = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
            md = monthdelta(months + 12 * years)
            return (td, md)

        def create_week_delta(weeks):
            return (timedelta(weeks=weeks), monthdelta(0))

        if len(args) == 0 and ('weeks' in kwargs):
            self.print_format = self.Format.WEEK
            try:
                (self.timedelta, self.monthdelta) = create_week_delta(**kwargs)
            except Exception as e:
                raise e
        else:
            self.print_format = self.Format.DURATION
            if len(args) == 0 and len(kwargs) == 2 and ('timedelta' in kwargs) and ('monthdelta' in kwargs):
                self.timedelta = kwargs['timedelta']
                self.monthdelta = kwargs['monthdelta']
            else:
                try:
                    (self.timedelta, self.monthdelta) = create_deltas(**resolve_args(args, kwargs))
                except Exception as e:
                    raise e

    @staticmethod
    def from_datetimes(start, end):
        (td, md) = (end.replace(month=start.month, year=start.year) - start,
            monthdelta((end.month - start.month) + 12 * (end.year - start.year)))
        return duration(timedelta=td, monthdelta=md)

    def string(self, print_format=None):
        _format = print_format or self.print_format
        if _format == self.Format.DURATION:
            return self.duration_format()
        elif _format == self.Format.WEEK:
            return self.week_format()
        else:
            return self.datetime_format(print_format)

    def week_format(self):
        weeks = self.timedelta.days // 7
        return 'P%iW' % weeks

    def components(self):
        return (self.monthdelta.months / 12, self.monthdelta.months % 12,
            self.timedelta.days, self.timedelta.seconds // 3600,
            self.timedelta.seconds // 60 % 60, self.timedelta.seconds % 60,
            self.timedelta.total_seconds())

    def duration_format(self):
        (years, months, days, hours, minutes, seconds, total_seconds) = self.components()

        y = '%iY' % years if years else ''
        mo = '%iM' % months if months else ''
        d = '%iD' % days if days else ''
        h = '%iH' % hours if hours else ''
        m = '%iM' % minutes if minutes else ''
        ms = str(total_seconds).split('.')[1].rstrip('0')
        s = '%01d' % seconds if seconds else ''
        div = '.' if ms else ''
        secs = 'S' if s or ms else ''

        return 'P%s%s%sT%s%s%s%s%s%s' % (y, mo, d, h, m, s, div, ms, secs)

    def datetime_format(self, print_format=None):
        _format = print_format or self.print_format
        (years, months, days, hours, minutes, seconds, microseconds) = self.components()

        y = '%04d' % years
        mo = '%02d' % months
        d = '%02d' % days
        h = '%02d' % hours
        m = '%02d' % minutes
        s = '%02d.%s' % (seconds, str(float(microseconds) / 10**6)[2:5].rstrip('0')) if microseconds else '%02d' % seconds

        if _format == self.Format.BASIC: 
            return 'P%s%s%sT%s%s%s' % (y, mo, d, h, m, s)
        else:
            return 'P%s-%s-%sT%s:%s:%s' % (y, mo, d, h, m, s)

    def __iter__(self):
        yield self.timedelta
        yield self.monthdelta

    def __repr__(self):
        return 'iso8601utils.duration(%s)' % self.string()

    def __str__(self):
        return self.__repr__()

    def __add__(self, other):
        if isinstance(other, duration):
            return duration(timedelta=(self.timedelta + other.timedelta),
                monthdelta=(self.monthdelta + other.monthdelta))
        if isinstance(other, datetime):
            return other + self.timedelta + self.monthdelta
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, duration):
            return duration(timedelta=(self.timedelta - other.timedelta),
                monthdelta=(self.monthdelta - other.monthdelta))
        if isinstance(other, datetime):
            return other - self.timedelta - self.monthdelta
        return NotImplemented

    def __mul__(self, other):
        return duration(timedelta=(other * self.timedelta),
            monthdelta=(other * self.monthdelta))

    def __div__(self, other):
        return duration(timedelta=(self.timedelta / other),
            monthdelta=(self.monthdelta / other))

    def __floordiv__(self, other):
        return duration(timedelta=(self.timedelta // other),
            monthdelta=(self.monthdelta // other))

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __neg__(self, other):
        return duration(timedelta=-self.timedelta, monthdelta=-self.monthdelta)

    def __pos__(self, other):
        return duration(timedelta=self.timedelta, monthdelta=self.monthdelta)

    def __abs__(self):
        return duration(timedelta=abs(self.timedelta), monthdelta=abs(self.monthdelta))

    def __bool__(self):
        return bool(self.timedelta) and bool(self.monthdelta)

    def __eq__(self, other):
        return (self.timedelta == other.timedelta) and (self.monthdelta == other.monthdelta)

    def __ne__(self, other):
        return (self.timedelta != other.timedelta) or (self.monthdelta != other.monthdelta)

    def __ge__(self, other):
        now = datetime.now()
        return now + self.timedelta + self.monthdelta >= now + other.timedelta + other.monthdelta

    def __gt__(self, other):
        now = datetime.now()
        return now + self.timedelta + self.monthdelta > now + other.timedelta + other.monthdelta

    def __le__(self, other):
        now = datetime.now()
        return now + self.timedelta + self.monthdelta <= now + other.timedelta + other.monthdelta

    def __lt__(self, other):
        now = datetime.now()
        return now + self.timedelta + self.monthdelta < now + other.timedelta + other.monthdelta

    def __hash__(self):
        return hash((self.timedelta, self.monthdelta))
