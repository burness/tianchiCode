#-*-coding:utf-8-*-
import pandas as pd
holiday_pd  = pd.read_csv('./data/date_holiday_result.txt')
holiday_pd.columns= ['date','holiday_type']
for line in ['线路6','线路11']:
    bus_line_name = './data/bus_count/final_'+line+'_bus_count.txt'
    bus_line_count = pd.read_csv(bus_line_name)
    bus_line_count.columns=['date','time','bus_cnt']
    bus_line_count['date_val'] = pd.to_datetime(bus_line_count['date'])
    holiday_pd['date_val'] = pd.to_datetime(holiday_pd['date'])
    print bus_line_count.head()
    print holiday_pd.head()
    bus_line_count_holiday = pd.merge(bus_line_count,holiday_pd, on='date_val')
    print bus_line_count_holiday.head()
    bus_line_grouped = bus_line_count_holiday.groupby(['holiday_type','time'])['bus_cnt'].mean().astype(int)
    print bus_line_grouped
    bus_line_grouped_name = './data/bus_count/gd_'+line+'_bus_aver_final.txt'
    bus_line_grouped.to_csv(bus_line_grouped_name)