# -*- coding: UTF-8 -*-
import re


# Parse times of the hh:mm:ss(.|,)sss, hh:mm:ss, hh:mm,
# hhmmss(.|,)sss, hhmmss, hhmm, and hh
# with a timezone offset of Z, ±hh:mm, ±hhmm, or ±hh
time = re.compile(
    r'^(?P<hour>([0,1][0-9]|2[0-4]))((:?)(?P<minute>[0-5][0-9])((\4)(?P<second>[0-5][0-9])((\.|,)(?P<millisecond>\d+))?)?)?'
    r'(Z|((?P<sign>(\+|-))((?P<offset_hour>([0,1][0-9]|2[0-4]))(:?(?P<offset_minute>[0-5][0-9]))?))?)$')


# Parse dates of the form YYYY-MM-DD, YYYY-MM,
# YYYYMMDD, YYYYMM, and YYYY
date_calendar = re.compile(r'^(?P<year>\d{4})((-?)(?P<month>(0[1-9]|1[0-2]))((\3)(?P<day>(0[1-9]|[1,2][0-9]|3[0,1])))?)?$')


# Parse dates of the form YYYY-MM-DD and YYYYMMDD
date_calendar_strict = re.compile(r'^(?P<year>\d{4})((-?)(?P<month>(0[1-9]|1[0-2]))((\3)(?P<day>(0[1-9]|[1,2][0-9]|3[0,1]))))$')


# Parse dates of the form YYYY-MM-DD, YYYY-MM, YYYYMMDD and YYYYMM
date_calendar_partial_0 = re.compile(r'^(?P<year>\d{4})((-?)(?P<month>(0[1-9]|1[0-2]))((\3)(?P<day>(0[1-9]|[1,2][0-9]|3[0,1])))?)$')


# Parse dates of the form MM-DD and MMDD
date_calendar_partial_1 = re.compile(r'^((?P<month>(0[1-9]|1[0-2]))(-?))?(?P<day>(0[1-9]|[1,2][0-9]|3[0,1]))$')


# Parse dates of the form --MM-DD and --MMDD
date_calendar_no_year = re.compile(r'^--(?P<month>(0[1-9]|1[0-2]))(-?)(?P<day>(0[1-9]|[1,2][0-9]|3[0,1]))$')


# Parse week dates of the form YYYY-Www, YYYY-Www-D, YYYYWww, and YYYYWwwD
date_week = re.compile(r'^(?P<year>\d{4})((-?)W(?P<week>(0[1-9]|[1-4][0-9]|5[0-3])))((\3)(?P<day>[1-7]))?$', re.IGNORECASE)


# Parse week dates of the form YYYYWwwD
date_week_strict = re.compile(r'^(?P<year>\d{4})((-?)W(?P<week>(0[1-9]|[1-4][0-9]|5[0-3])))((\3)(?P<day>[1-7]))$', re.IGNORECASE)


# Parse ordinal dates of the form YYYY-DDD and YYYYDDD
date_ordinal = re.compile(r'^(?P<year>\d{4})(-?)(?P<day>(0[0-9][1-9]|[1,2][0-9][0-9]|3[0-5][0-9]|36[0-6]))$')


dates = [date_calendar, date_calendar_no_year, date_week, date_ordinal]


dates_strict = [date_calendar_strict, date_week_strict, date_ordinal]


dates_partial = [date_calendar_partial_0, date_calendar_partial_1]


# Parse durations of the form PnYnMnDTnHnMnS
duration_standard = re.compile(
    r'^P((?P<years>(\d+(\.\d*)?|\.\d+))Y)?'
    r'((?P<months>(\d+(\.\d*)?|\.\d+))M)?'
    r'((?P<days>(\d+(\.\d*)?|\.\d+))D)?'
    r'(T((?P<hours>(\d+(\.\d*)?|\.\d+))H)?'
    r'((?P<minutes>(\d+(\.\d*)?|\.\d+))M)?'
    r'((?P<seconds>(\d+(\.\d*)?|\.\d+))S)?)?$',
    re.IGNORECASE)


# Parse durations of the form PYYYYMMDDThhmmss and P[YYYY]-[MM]-[DD]T[hh]:[mm]:[ss]
duration_datetime = re.compile(r'^P(?P<years>\d{4})(-?)(?P<months>(0[1-9]|1[0-2]))(\2)(?P<days>(0[1-9]|[1,2][0-9]|3[0,1]))T'
    r'(?P<hours>([0,1][0-9]|2[0-4]))(:?)(?P<minutes>[0-5][0-9])(\10)(?P<seconds>[0-5][0-9])$', re.IGNORECASE)


# ([0-9]*[.])?[0-9]+
# Parse durations of the form PnW
duration_week = re.compile(r'^P(?P<weeks>([0-9]*[.])?[0-9]+)W$', re.IGNORECASE)


durations = [duration_standard, duration_datetime, duration_week]


# Parse interval repeat component of the form Rn
repeat = re.compile(r'^R(?P<repeat>\d)?$', re.IGNORECASE)
