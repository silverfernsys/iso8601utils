import re


# Parse times of the hh:mm:ss.sss, hh:mm:ss, hh:mm, or hh
time_form_0 = re.compile(
    r'^(?P<hour>[0-2][0-9])(:(?P<minute>[0-5][0-9])(:(?P<second>[0-5][0-9])(\.(?P<millisecond>\d+))?)?)?'
    r'(Z|((?P<sign>(\+|-))((?P<offset_hour>[0-2][0-9])(:?(?P<offset_minute>[0-5][0-9]))?))?)$')


# Parse times of the form hhmmss.sss, hhmmss, hhmm, or hh
time_form_1 = re.compile(
    r'^(?P<hour>[0-2][0-9])((?P<minute>[0-5][0-9])((?P<second>[0-5][0-9])(\.(?P<millisecond>\d+))?)?)?'
    r'(Z|((?P<sign>(\+|-))((?P<offset_hour>[0-2][0-9])(:?(?P<offset_minute>[0-5][0-9]))?))?)$')


times = [time_form_0, time_form_1]


# Parse dates of the form YYYY-MM-DD or YYYY-MM
date_calendar_form_0 = re.compile(
    r'^(?P<year>\d{4})(-(?P<month>\d{2})(-(?P<day>\d{2}))?)?$')


# Parse dates of the form YYYYMMDD
date_calendar_form_1 = re.compile(
    r'^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})$')


# Parse dates of the form --MM-DD or --MMDD
date_calendar_form_2 = re.compile(
    r'^--(?P<month>\d{2})(-?)(?P<day>\d{2})$')


date_calendars = [date_calendar_form_0, date_calendar_form_1, date_calendar_form_2]


# Parse week dates of the form YYYYWww or YYYYWwwD
date_week_0 = re.compile(
    r'^(?P<year>\d{4})(W(?P<week>\d{2}))((?P<day>\d{1})?)$', re.IGNORECASE)


# Parse week dates of the form YYYY-Www or YYYY-Www-D
date_week_1 = re.compile(
    r'^(?P<year>\d{4})(-W(?P<week>\d{2}))((-(?P<day>\d{1}))?)$', re.IGNORECASE)


date_weeks = [date_week_0, date_week_1]


dates = date_calendars + date_weeks


# Parse ordinal dates of the form YYYY-DDD or YYYYDDD
date_ordinal = re.compile(
    r'^(?P<year>\d{4})(-?)(?P<day>\d{3})$')


# Parse durations of the form PnYnMnDTnHnMnS
duration_form_0 = re.compile(
    r'^P((?P<year>(\d+(\.\d*)?|\.\d+))Y)?'
    r'((?P<month>(\d+(\.\d*)?|\.\d+))M)?'
    r'((?P<day>(\d+(\.\d*)?|\.\d+))D)?'
    r'(T((?P<hour>(\d+(\.\d*)?|\.\d+))H)?'
    r'((?P<minute>(\d+(\.\d*)?|\.\d+))M)?'
    r'((?P<second>(\d+(\.\d*)?|\.\d+))S)?)?$',
    re.IGNORECASE)


# Parse durations of the form PYYYYMMDDThhmmss
duration_form_1 = re.compile(
    r'^P(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})T'
    r'(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})$',
    re.IGNORECASE)


# Parse durations of the form P[YYYY]-[MM]-[DD]T[hh]:[mm]:[ss]
duration_form_2 = re.compile(
    r'^P(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})T'
    r'(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})$',
    re.IGNORECASE)

# ([0-9]*[.])?[0-9]+
# Parse durations of the form PnW
duration_week_form = re.compile(
    r'^P(?P<week>([0-9]*[.])?[0-9]+)W$', # r'^P(?P<week>(\d+(\.\d*)?|\.\d+))W$',
    re.IGNORECASE)


duration_standard_forms = [duration_form_0, duration_form_1, duration_form_2]


durations = [duration_form_0, duration_form_1, duration_form_2, duration_week_form]


# Parse interval repeat component of the form Rn
repeat = re.compile(
    r'^R(?P<repeat>\d)?$',
    re.IGNORECASE)
