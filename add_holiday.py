#-*-coding:utf-8-*
__author__ = 'burness'
import pandas as pd
def add_holiday(gd_train_line_pd_weather):
    gd_train_date_holiday = pd.read_csv('./data/date_holiday_result.txt')
    gd_train_date_holiday.columns=['date','holiday']
    gd_train_date_holiday['date']=pd.to_datetime(gd_train_date_holiday['date'])
    gd_train_line_pd_weather['date_val']=pd.to_datetime(gd_train_line_pd_weather['date'])
    gd_train_line_pd_weather['dayofweek']=gd_train_line_pd_weather['date_val'].apply(lambda x: x.dayofweek)

    gd_train_line_pd_weather_holiday = pd.merge(gd_train_line_pd_weather,gd_train_date_holiday,left_on='date_val',right_on='date')
    return gd_train_line_pd_weather_holiday