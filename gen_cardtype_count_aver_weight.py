#-*-coding:utf-8-*-
import pandas as pd
holiday_pd  = pd.read_csv('./data/date_holiday_result.txt')
holiday_pd.columns= ['date','holiday_type']
for line in ['线路6','线路11']:
    cardtype_weight = './data/cardtype_%s_count_weight.txt'%line
    cardtype_weight_data = pd.read_csv(cardtype_weight)
    cardtype_weight_data['date_val'] = pd.to_datetime(cardtype_weight_data['date'])
    holiday_pd['date_val'] = pd.to_datetime(holiday_pd['date'])
    print cardtype_weight_data.head()
    print holiday_pd.head()
    cardtype_weight_holiday = pd.merge(cardtype_weight_data,holiday_pd, on='date_val')
    print cardtype_weight_holiday.head()
    cardtype_weight_grouped = cardtype_weight_holiday.groupby(['holiday_type','time'])['cardtype0_weight',
                                                                                       'cardtype1_weight',
                                                                                       'cardtype2_weight',
                                                                                       'cardtype3_weight',
                                                                                       'cardtype4_weight',
                                                                                       'cardtype5_weight',
                                                                                       'cardtype6_weight'].mean().astype(float)
    print cardtype_weight_grouped
    bus_line_grouped_name = './data/gd_'+line+'_aver_weight_final.txt'
    cardtype_weight_grouped.to_csv(bus_line_grouped_name)