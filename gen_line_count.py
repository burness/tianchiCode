#-*-coding:utf-8-*-
__author__ = 'burness'
import pandas as pd
gd_train_data = pd.read_csv('./data/gd_train_data.txt',header=False)
gd_train_data.columns = ['use_city','line_name','terminal_id','card_id','create_city','deal_time','card_type']

# 每天线路的客流count
# gd_train_count =  gd_train_data.groupby(['line_name','deal_time']).count()
for line in ['线路6','线路11']:
    gd_train_line_count = gd_train_data[gd_train_data['line_name']==line]['deal_time'].value_counts()
    count_name = './data/count/'+line+'_count.txt'
    gd_train_line_count.to_csv(count_name)
# print gd_train_count
# print gd_train_data.head(10)