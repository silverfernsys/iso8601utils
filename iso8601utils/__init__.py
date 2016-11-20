__version__='0.1.1'

from collections import Iterable
from datetime import datetime, timedelta
from enum import Enum
from monthdelta import MonthDelta as monthdelta

try:
    from itertools import izip as zip
except:
    pass


class duration(object):
    Format = Enum('Format', 'DURATION BASIC EXTENDED WEEK')
    # TODO: Implement comparison operators
    # https://bitbucket.org/jessaustin/monthdelta/src/d9da1b1a9f82a9886eebd0a7fe3f11331a13d596/monthdelta.py
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
            self.timedelta.microseconds)

    def duration_format(self):
        (years, months, days, hours, minutes, seconds, microseconds) = self.components()

        if years:
            y = '%iY' % years
        else:
            y = ''
        if months:
            mo = '%iM' % months
        else:
            mo = ''
        if days:
            d = '%iD' % days
        else:
            d = ''
        if hours:
            h = '%iH' % hours
        else:
            h = ''
        if minutes:
            m = '%iM' % minutes
        else:
            m = ''
        if microseconds:
            s = '%01d' % seconds
            ms = str(float(microseconds) / 10**6)[2:5].rstrip('0')
        else:
            if seconds:
                s = '%01d' % seconds
            else:
                s = '' 
            ms = ''
        if seconds or microseconds:
            secs = '%s.%sS' % (s, ms)
        else:
            secs = ''
        return 'P%s%s%sT%s%s%s' % (y, mo, d, h, m, secs)

    def datetime_format(self, print_format=None):
        _format = print_format or self.print_format
        (years, months, days, hours, minutes, seconds, microseconds) = self.components()

        y = '%04d' % years
        mo = '%02d' % months
        d = '%02d' % days
        h = '%02d' % hours
        m = '%02d' % minutes
        if microseconds:
            s = '%02d.%s' % (seconds, str(float(microseconds) / 10**6)[2:5].rstrip('0'))
        else:
            s = '%02d' % seconds

        if _format == self.Format.BASIC: 
            return 'P%s%s%sT%s%s%s' % (y, mo, d, h, m, secs)
        else:
            return 'P%s-%s-%sT%s:%s:%s' % (y, mo, d, h, m, secs)

    def __repr__(self):
        return self.string()

    def __str__(self):
        return self.__repr__()

    def __add__(self, other):
        return duration(timedelta=(self.timedelta + other.timedelta),
            monthdelta=(self.monthdelta + other.monthdelta))

    def __sub__(self, other):
        return duration(timedelta=(self.timedelta - other.timedelta),
            monthdelta=(self.monthdelta - other.monthdelta))

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
        return other.__sub__(self)

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


class interval(Iterable):
    Format = Enum('Format', 'START_END START_DURATION DURATION_END DURATION')

    def __init__(self, **kwargs):
        print('kwargs: %s' % kwargs)
        expected_kwargs = set(('start', 'end', 'duration', 'repeats'))
        required_kwargs = set(('start', 'end', 'duration'))
        required_count = 2

        unexpected_kwargs = set(kwargs) - expected_kwargs
        if unexpected_kwargs:
            raise ValueError('Unexpected keyword arguments %s.' % ', '.join([k for k in unexpected_kwargs]))
        missing_count = required_count - len(kwargs)
        if missing_count > 0:
            missing_kwargs = required_kwargs - set(kwargs)
            raise ValueError('Expecting %d of %s.' % (missing_count, ', '.join([k for k in missing_kwargs])))
        if 'start' in kwargs and 'end' in kwargs:
            self.start = kwargs['start']
            self.end = kwargs['end']
            self.duration = duration.from_datetimes(self.start, self.end)
        elif 'start' in kwargs and 'duration' in kwargs:
            self.start = kwargs['start']
            self.duration = kwargs['duration']
            self.end = self.start + self.duration.timedelta + self.duration.monthdelta
        elif 'end' in kwargs and 'duration' in kwargs:
            self.end = kwargs['end']
            self.duration = kwargs['duration']
            self.start = self.end - self.duration.timedelta - self.duration.monthdelta
        self.repeats = kwargs.get('repeats', 0)

    def string(self, format=None, component_formats=None):
        format_ = format or self.Format.START_END
        component_formats = component_formats
        if self.repeats:
            if self.repeats == float('inf'):
                r = 'R/'
            else:
                r = 'R%d/' % self.repeats
        else:
            r = ''      
        if format_ == self.Format.START_END:
            s = self.start.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            e = self.end.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            return '%s%s/%s' % (r, s, e)
        elif format_ == self.Format.START_DURATION:
            s = self.start.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            d = self.duration.string()
            return '%s%s/%s' % (r, s, d)
        elif format_ == self.Format.DURATION_END:
            d = self.duration.string()
            e = self.end.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
            return '%s%s/%s' % (r, d, e)
        else:
            return self.duration.string()

    def __iter__(self):
        return self

    def __repr__(self):
        return 'iso8601utils.interval(%s)' % self.string()

    def __str__(self):
        return self.__repr__()

    def __bool__(self):
        return bool(self.duration)

    def __eq__(self, other):
        return (self.start == other.start and self.end == other.end
            and self.duration == other.duration and self.repeats == other.repeats)

    def __ne__(self, other):
        return (self.start != other.start or self.end != other.end
            or self.duration != other.duration or self.repeats != other.repeats)

    def __hash__(self):
        return hash((self.start, self.end, self.duration, self.repeats))

