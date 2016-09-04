import re


interval = re.compile(
    r'^(P((?P<s_i_year>(\d+(\.\d*)?|\.\d+))Y)?'
    r'((?P<s_i_month>(\d+(\.\d*)?|\.\d+))M)?'
    r'((?P<s_i_week>(\d+(\.\d*)?|\.\d+))W)?'
    r'((?P<s_i_day>(\d+(\.\d*)?|\.\d+))D)?'
    r'(T((?P<s_i_hour>(\d+(\.\d*)?|\.\d+))H)?'
    r'((?P<s_i_minute>(\d+(\.\d*)?|\.\d+))M)?'
    r'((?P<s_i_second>(\d+(\.\d*)?|\.\d+))S)?)?|'
    r'(?P<s_dt_year>\d{4})-(?P<s_dt_month>\d{2})-(?P<s_dt_day>\d{2})'
    r'(T(?P<s_dt_hour>\d{2}):(?P<s_dt_minute>\d{2}):'
    r'(?P<s_dt_second>(\d{2}))(\.(?P<s_dt_microsecond>\d+))?Z)?)(/'
    r'(P((?P<e_i_year>(\d+(\.\d*)?|\.\d+))Y)?'
    r'((?P<e_i_month>(\d+(\.\d*)?|\.\d+))M)?'
    r'((?P<e_i_week>(\d+(\.\d*)?|\.\d+))W)?'
    r'((?P<e_i_day>(\d+(\.\d*)?|\.\d+))D)?'
    r'(T((?P<e_i_hour>(\d+(\.\d*)?|\.\d+))H)?'
    r'((?P<e_i_minute>(\d+(\.\d*)?|\.\d+))M)?'
    r'((?P<e_i_second>(\d+(\.\d*)?|\.\d+))S)?)?|'
    r'(?P<e_dt_year>\d{4})-(?P<e_dt_month>\d{2})-(?P<e_dt_day>\d{2})'
    r'(T(?P<e_dt_hour>\d{2}):(?P<e_dt_minute>\d{2}):'
    r'(?P<e_dt_second>(\d{2}))(\.(?P<e_dt_microsecond>\d+))?Z)?))?$')


duration = re.compile(
    r'^P((?P<year>(\d+(\.\d*)?|\.\d+))Y)?'
    r'((?P<month>(\d+(\.\d*)?|\.\d+))M)?'
    r'((?P<week>(\d+(\.\d*)?|\.\d+))W)?'
    r'((?P<day>(\d+(\.\d*)?|\.\d+))D)?'
    r'(T((?P<hour>(\d+(\.\d*)?|\.\d+))H)?'
    r'((?P<minute>(\d+(\.\d*)?|\.\d+))M)?'
    r'((?P<second>(\d+(\.\d*)?|\.\d+))S)?)?$')
