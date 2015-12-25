#-*-coding:utf-8-*-
'''
这个脚本用来预测20150101-20150107的数据,不经过dummies
'''
import pandas as pd
import copy
from sklearn.externals import joblib
__author__ = 'burness'
test_data = pd.read_csv('./data/test_data_final.csv',header=None)
print test_data.count()
test_data.columns = ['time','date','dayofweek','weatherA_val','weatherB_val','weatherPeriod','weatherE',
                     'temperatureA','temperatureB','temperaturePeriod','temperatureE','holiday']
# print test_data

final_data = test_data
# print test_data

for line in ['线路6','线路11']:
    model_name = './model/2015-11-26/traffic_GBDT_'+line+'.model'
    gd_model = joblib.load(model_name)
    # 增加time字段

    final_data = final_data[['date','time','dayofweek','weatherA_val',
                             'weatherB_val','weatherPeriod','weatherE',
                             'temperatureA','temperatureB','temperaturePeriod','temperatureE','holiday']]
    # print final_data
    bus_cnt_name= './data/bus_count/gd_'+line+'_bus_aver_final.txt'
    bus_cnt = pd.read_csv(bus_cnt_name)
    bus_cnt.columns = ['holiday','time','bus_cnt']
    final_data = pd.merge(final_data,bus_cnt,on=['holiday','time'])
    print final_data
    final_data.to_csv('./data/final_data_test.txt',index=False)
#
#     # print test_data_final
#     # test_data_final.to_csv('test.dat')
    final_data_train = final_data[['time','dayofweek','weatherA_val',
                                   'weatherB_val','weatherPeriod','weatherE',
                                   'temperatureA','temperatureB','temperaturePeriod','temperatureE','holiday','bus_cnt']]
    predict_label = gd_model.predict(final_data_train)
#     print predict_label
    result_data = pd.DataFrame()
    result_data['date'] = final_data['date'].str.split('-').str[0]+final_data['date'].str.split('-').str[1]+final_data['date'].str.split('-').str[2];
    result_data['time'] = final_data['time']
    result_data['cnt'] = pd.DataFrame(predict_label).astype(int)
    result_data['line'] = line
    result_name = './data/result/2015-11-26/traffic_'+line+'GBDT_result.txt'
    result_data.to_csv(result_name,index=False,header=False)
#
