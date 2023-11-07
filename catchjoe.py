import pytz
from datetime import datetime

def filter_joe_unique_values(_df, df_joe, ft_lists):
    for x in ft_lists:
        _joe = df_joe[x].drop_duplicates()
        _joe['joe'] = True
        _df = _df.merge(_joe, on=x, how='left').fillna(False)
        if x == ['location']:
            new_value = 'UTC'
        else:
            new_value = 'others'
        _df.loc[~_df['joe'], x] = new_value
        _df.drop('joe', 1, inplace=True)
    return _df

def europe_tz(x):
    europe_citys = [x[7:] for x in pytz.all_timezones if 'Europe' in x]
    for c in europe_citys:
        if c in x:
            x = f'Europe/{c}'
    return x

def get_localtime(_df):
    utc = pytz.timezone("UTC")
    _df['timezone'] = _df['location']
    _df['timezone'] = _df['timezone'].replace('Canada/Toronto','Canada/Eastern')
    _df['timezone'] = _df['timezone'].replace('Singapore/Singapore','Singapore')
    _df['timezone'] = _df['timezone'].str.replace('USA','US')
    _df['timezone'] = _df['timezone'].str.replace('Chicago','Central')
    _df['timezone'] = _df['timezone'].apply(europe_tz)
    _df['datetime'] = _df.apply(
        lambda x: datetime.strptime(f"{str(x['date'])[:10]} {x['time']}",
                                    '%Y-%m-%d %H:%M:%S').astimezone(utc)
    , 1)
    _df['local_time'] = _df.apply(
        lambda x: x['datetime'].tz_convert(x['timezone']), 1
    )
    _df['local_time'] = _df['local_time'].apply(
        lambda x: datetime.strptime(str(x)[:19], '%Y-%m-%d %H:%M:%S')
    )
    return _df