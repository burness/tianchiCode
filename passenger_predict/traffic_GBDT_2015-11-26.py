#-*-coding:utf-8-*-
'''
这个脚本用来训练为经过dummies的模型，并且保存
'''
__author__ = 'burness'
import pandas as pd
from add_holiday import add_holiday
from compute_error import compute_error
gd_lines_info = pd.read_csv('./data/gd_line_desc.txt')
gd_lines_info.columns=['line_name','stop_cnt','line_type']

gd_weather_info = pd.read_csv('./data/gd_weather_report.txt')
gd_weather_info.columns=['date','weather','temperature','wind_direction_force']

gd_lines_info['line_type_val']=gd_lines_info['line_type'].map({'广州市内':0,'广佛跨区域':1})

gd_lines_info=gd_lines_info.drop(['line_type'],axis=1)
for line in ['线路6','线路11']:
# for line in ['线路11']:
    train_count_file = './data/count/final_%s_count.txt'%line
    gd_train_line_pd = pd.read_csv(train_count_file)
    gd_train_line_pd.columns = ['date','time','cnt']
    # print gd_train_line_pd.count()
    gd_train_line_pd.head()
    # join the weather
    print gd_weather_info.columns
    gd_train_line_pd_weather = pd.merge(gd_train_line_pd,gd_weather_info,on='date')
    # print gd_train_line_pd_weather.count()
    gd_train_line_pd_weather['date_val']=pd.to_datetime(gd_train_line_pd_weather['date'])
    gd_train_line_pd_weather.head()
    gd_train_line_pd_weather['dayofweek']=gd_train_line_pd_weather['date_val'].apply(lambda x: x.dayofweek)
    gd_train_line_pd_weather['weatherA']=gd_train_line_pd_weather['weather'].str.split('/').str[0]
    gd_train_line_pd_weather['weatherB']=gd_train_line_pd_weather['weather'].str.split('/').str[1]
    gd_train_line_pd_weather['weatherA_val']=gd_train_line_pd_weather['weatherA'].map({'大到暴雨':0,'大雨':1,'中到大雨':2,'中雨':3,
                                                                                       '小到中雨':4,'雷阵雨':5,'阵雨':6,'小雨':7,'阴':8
                                                                                          ,'多云':9,'晴':10})
    gd_train_line_pd_weather['weatherB_val']=gd_train_line_pd_weather['weatherB'].map({'大到暴雨':0,'大雨':1,'中到大雨':2,'中雨':3,
                                                                                       '小到中雨':4,'雷阵雨':5,'阵雨':6,'小雨':7,'阴':8
                                                                                          ,'多云':9,'晴':10})
    gd_train_line_pd_weather[['weatherA_val','weatherB_val']]=gd_train_line_pd_weather[['weatherA_val','weatherB_val']].astype(int)
    gd_train_line_pd_weather['weatherPeriod']=abs(gd_train_line_pd_weather['weatherA_val']-gd_train_line_pd_weather['weatherB_val'])
    gd_train_line_pd_weather['weatherE']=(gd_train_line_pd_weather['weatherA_val']+gd_train_line_pd_weather['weatherB_val'])/2.0
    # gd_train_line_pd_weather.dtypes
    gd_train_line_pd_weather=gd_train_line_pd_weather.drop(['weather','weatherA','weatherB'],axis=1)
    gd_train_line_pd_weather['temperatureA']=gd_train_line_pd_weather['temperature'].str.split('/').str[0].str.extract('(\d+)')
    gd_train_line_pd_weather['temperatureB']=gd_train_line_pd_weather['temperature'].str.split('/').str[1].str.extract('(\d+)')
    gd_train_line_pd_weather[['temperatureA','temperatureB']]=gd_train_line_pd_weather[['temperatureA','temperatureB']].astype(float)
    gd_train_line_pd_weather['temperaturePeriod']=abs(gd_train_line_pd_weather['temperatureA']-gd_train_line_pd_weather['temperatureB'])
    gd_train_line_pd_weather['temperatureE']=(gd_train_line_pd_weather['temperatureA']+gd_train_line_pd_weather['temperatureB'])/2.0

    # 增加bus数量
    bus_line_name = './data/bus_count/final_'+line+'_bus_count.txt'
    bus_line = pd.read_csv(bus_line_name)
    bus_line.columns=['date','time','bus_cnt']
    bus_line['date_val'] = pd.to_datetime(bus_line['date'])
    bus_line = bus_line.drop('date',axis=1)
    # print bus_line.dtypes
    # print gd_train_line_pd_weather.dtypes
    gd_train_line_pd_weather = pd.merge(gd_train_line_pd_weather,bus_line,on=['date_val','time'])
    # print gd_train_line_pd_weather.columns

    # 滤除非6点到21点得数据
    # print gd_train_line_pd_weather[gd_train_line_pd_weather['time']==23]
    gd_train_line_pd_weather = gd_train_line_pd_weather[gd_train_line_pd_weather['time']>=6]
    gd_train_line_pd_weather = gd_train_line_pd_weather[gd_train_line_pd_weather['time']<=21]

    # 加上holiday信息
    gd_train_line_pd_weather = add_holiday(gd_train_line_pd_weather)
    print gd_train_line_pd_weather.head()
    print gd_train_line_pd_weather.count()

    gd_train_line_pd_final = gd_train_line_pd_weather[['cnt','time','dayofweek','weatherA_val',
                                                      'weatherB_val','weatherPeriod','weatherE',
                                                      'temperatureA','temperatureB','temperaturePeriod','temperatureE','holiday','bus_cnt']]

    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn import grid_search
    data=gd_train_line_pd_final[['time','dayofweek','weatherA_val','weatherB_val','weatherPeriod','weatherE',
                                 'temperatureA','temperatureB','temperaturePeriod','temperatureE','holiday','bus_cnt']]
    labels = gd_train_line_pd_final['cnt']
    # # # print data.head(40)
    from sklearn.cross_validation import train_test_split
    train_data,test_data,train_labels,test_labels=train_test_split(data,labels,test_size=7*15)
    est = GradientBoostingRegressor()
    parameters={'loss':('ls', 'lad', 'huber', 'quantile'),'learning_rate':[0.04*(i+1) for i in range(25)],
                'n_estimators':[75,100,125,150],'max_depth':[2,3,4]}
    clf=grid_search.GridSearchCV(est,parameters)
    print 'performing grid_searching...'
    print 'parameters:'
    from time import time
    t0=time()
    clf.fit(train_data,train_labels)
    print 'grid_searching takes %0.3fs'%(time()-t0)
    best_parameters=clf.best_params_

    for para_name in sorted(parameters.keys()):
        print para_name
        print best_parameters[para_name]
    #
    #
    #
    est.set_params(learning_rate=best_parameters['learning_rate'],
                   loss=best_parameters['loss'],max_depth=best_parameters['max_depth'],n_estimators=best_parameters['n_estimators'])
    est.fit(train_data,train_labels)
    print '保存model....'
    from sklearn.externals import joblib
    model_name = './model/2015-11-26/traffic_GBDT_'+line+'.model'
    joblib.dump(est,model_name)


    # validation procee
    est = joblib.load('./model/2015-11-26/traffic_GBDT_'+line+'.model')
    sum = 0.0
    for i in range(200):
        val_train_data,val_test_data,val_train_labels,val_test_labels=train_test_split(data,labels,test_size=7*15)
        predict_labels = est.predict(val_test_data)
        print predict_labels
        error = compute_error(predict_labels,val_test_labels)
        print 'val error: %f '% error
        sum+=error
    print 'averge error: %f'%(sum/200)
