from collections import Iterable
from iso8601utils.duration import duration
from enum import Enum


class interval(Iterable):
    Format = Enum('Format', 'START_END START_DURATION DURATION_END DURATION')
    INFINITE = float('inf')

    def __init__(self, **kwargs):
        valid_kwargs = set(('start', 'end', 'duration', 'repeats'))
        required_kwargs = set(('start', 'end', 'duration'))
        required_count = 2

        invalid_kwargs = set(kwargs) - valid_kwargs
        if invalid_kwargs:
            raise ValueError('Unexpected keyword arguments %s.' % ', '.join([k for k in invalid_kwargs]))
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

        if self.repeats != self.INFINITE:
            self.repeats = int(self.repeats)

    def string(self, format=None, component_formats=None):
        format_ = format or self.Format.START_END
        component_formats = component_formats
        r = 'R/' if self.repeats == self.INFINITE else ('R%d/' % self.repeats if self.repeats else '')     
        if format_ == self.Format.START_END:
            s = self.start.strftime('%Y-%m-%dT%H:%M:%S.%f%Z')
            e = self.end.strftime('%Y-%m-%dT%H:%M:%S.%f%Z')
            return '%s%s/%s' % (r, s, e)
        elif format_ == self.Format.START_DURATION:
            s = self.start.strftime('%Y-%m-%dT%H:%M:%S.%f%Z')
            d = self.duration.string()
            return '%s%s/%s' % (r, s, d)
        elif format_ == self.Format.DURATION_END:
            d = self.duration.string()
            e = self.end.strftime('%Y-%m-%dT%H:%M:%S.%f%Z')
            return '%s%s/%s' % (r, d, e)
        else:
            return self.duration.string()

    def __iter__(self):
        yield self.repeats
        yield self.start
        yield self.end
        yield self.duration

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
