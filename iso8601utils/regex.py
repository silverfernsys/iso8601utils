import re


time_form_0 = re.compile(
    r'^(?P<hour>[0-2][0-9])(:(?P<minute>[0-5][0-9])(:(?P<second>[0-5][0-9])(\.(?P<microsecond>\d+))?)?)?'
    r'(Z|((?P<sign>(\+|-))((?P<offset_hour>[0-2][0-9])(:?(?P<offset_minute>[0-5][0-9]))?))?)$')


time_form_1 = re.compile(
    r'^(?P<hour>[0-2][0-9])((?P<minute>[0-5][0-9])((?P<second>[0-5][0-9])(\.(?P<microsecond>\d+))?)?)?'
    r'(Z|((?P<sign>(\+|-))((?P<offset_hour>[0-2][0-9])(:?(?P<offset_minute>[0-5][0-9]))?))?)$')


date_form_0 = re.compile(
    r'^(?P<year>\d{4})(-(?P<month>\d{2})(-(?P<day>\d{2}))?)?$')


date_form_1 = re.compile(
    r'^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})$')


date_form_2 = re.compile(
    r'^--(?P<month>\d{2})(-?)(?P<day>\d{2})$')


date_ordinal = re.compile(
    r'^(?P<year>\d{4})(-?)(?P<day>\d{3})$')


# Parse durations of the form PnYnMnDTnHnMnS
duration_form_0 = re.compile(
    r'^P((?P<year>(\d+(\.\d*)?|\.\d+))Y)?'
    r'((?P<month>(\d+(\.\d*)?|\.\d+))M)?'
    r'((?P<day>(\d+(\.\d*)?|\.\d+))D)?'
    r'(T((?P<hour>(\d+(\.\d*)?|\.\d+))H)?'
    r'((?P<minute>(\d+(\.\d*)?|\.\d+))M)?'
    r'((?P<second>(\d+(\.\d*)?|\.\d+))S)?)?$')


# Parse durations of the form PnW
duration_form_1 = re.compile(
    r'^P(?P<week>(\d+(\.\d*)?|\.\d+))W$')


# Parse durations of the form PYYYYMMDDThhmmss
duration_form_2 = re.compile(
    r'^P(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})T'
    r'(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})$')


# Parse durations of the form P[YYYY]-[MM]-[DD]T[hh]:[mm]:[ss]
duration_form_3 = re.compile(
    r'^P(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})T'
    r'(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2})$')


repeat = re.compile(
    r'^R(?P<repeat>\d)?$')
