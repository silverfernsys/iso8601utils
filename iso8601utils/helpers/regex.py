import re


# Parse times of the hh:mm:ss.sss, hh:mm:ss, hh:mm, or hh
time_simple = re.compile(
    r'^(?P<hour>[0-2][0-9])(:(?P<minute>[0-5][0-9])(:(?P<second>[0-5][0-9])(\.(?P<millisecond>\d+))?)?)?'
    r'(Z|((?P<sign>(\+|-))((?P<offset_hour>[0-2][0-9])(:?(?P<offset_minute>[0-5][0-9]))?))?)$')


# Parse times of the form hhmmss.sss, hhmmss, hhmm, or hh
time_extended = re.compile(
    r'^(?P<hour>[0-2][0-9])((?P<minute>[0-5][0-9])((?P<second>[0-5][0-9])(\.(?P<millisecond>\d+))?)?)?'
    r'(Z|((?P<sign>(\+|-))((?P<offset_hour>[0-2][0-9])(:?(?P<offset_minute>[0-5][0-9]))?))?)$')


times = [time_simple, time_extended]


# Parse dates of the form YYYYMMDD
date_calendar_simple = re.compile(
    r'^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})$')


# Parse dates of the form YYYY-MM-DD or YYYY-MM
date_calendar_extended = re.compile(
    r'^(?P<year>\d{4})(-(?P<month>\d{2})(-(?P<day>\d{2}))?)?$')


# Parse dates of the form --MM-DD or --MMDD
date_calendar_no_year = re.compile(
    r'^--(?P<month>\d{2})(-?)(?P<day>\d{2})$')


# Parse week dates of the form YYYYWww or YYYYWwwD
date_week_simple = re.compile(
    r'^(?P<year>\d{4})(W(?P<week>\d{2}))((?P<day>\d{1})?)$', re.IGNORECASE)


# Parse week dates of the form YYYY-Www or YYYY-Www-D
date_week_extended = re.compile(
    r'^(?P<year>\d{4})(-W(?P<week>\d{2}))((-(?P<day>\d{1}))?)$', re.IGNORECASE)


# Parse ordinal dates of the form YYYY-DDD or YYYYDDD
date_ordinal = re.compile(
    r'^(?P<year>\d{4})(-?)(?P<day>\d{3})$')


dates = [date_calendar_simple, date_calendar_extended, date_calendar_no_year,
    date_week_simple, date_week_extended, date_ordinal]


# Parse durations of the form PnYnMnDTnHnMnS
duration_standard = re.compile(
    r'^P((?P<years>(\d+(\.\d*)?|\.\d+))Y)?'
    r'((?P<months>(\d+(\.\d*)?|\.\d+))M)?'
    r'((?P<days>(\d+(\.\d*)?|\.\d+))D)?'
    r'(T((?P<hours>(\d+(\.\d*)?|\.\d+))H)?'
    r'((?P<minutes>(\d+(\.\d*)?|\.\d+))M)?'
    r'((?P<seconds>(\d+(\.\d*)?|\.\d+))S)?)?$',
    re.IGNORECASE)


# Parse durations of the form PYYYYMMDDThhmmss
duration_datetime_simple = re.compile(
    r'^P(?P<years>\d{4})(?P<months>\d{2})(?P<days>\d{2})T'
    r'(?P<hours>\d{2})(?P<minutes>\d{2})(?P<seconds>\d{2})$',
    re.IGNORECASE)


# Parse durations of the form P[YYYY]-[MM]-[DD]T[hh]:[mm]:[ss]
duration_datetime_extended = re.compile(
    r'^P(?P<years>\d{4})-(?P<months>\d{2})-(?P<days>\d{2})T'
    r'(?P<hours>\d{2}):(?P<minutes>\d{2}):(?P<seconds>\d{2})$',
    re.IGNORECASE)

# ([0-9]*[.])?[0-9]+
# Parse durations of the form PnW
duration_week = re.compile(
    r'^P(?P<weeks>([0-9]*[.])?[0-9]+)W$',
    re.IGNORECASE)


durations = [duration_standard, duration_datetime_simple,
    duration_datetime_extended, duration_week]


# Parse interval repeat component of the form Rn
repeat = re.compile(
    r'^R(?P<repeat>\d)?$',
    re.IGNORECASE)
