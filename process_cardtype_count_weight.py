#-*-coding:utf-8-*
import pandas as pd
# def compute_weight(pd):

for line in ['线路6','线路11']:
    cardtype_count_name = './data/count/final_'+line+'_count_cardtype.txt'
    gd_cardtype_cnt = pd.read_csv(cardtype_count_name,header=None)
    gd_cardtype_cnt.columns = ['card_type','date','time','cardtype_cnt']
    cardtype_list = sorted(gd_cardtype_cnt['card_type'].unique())
    print len(cardtype_list)
    cardtype_dict = dict(zip(cardtype_list,range(len(cardtype_list)+1)))
    gd_cardtype_cnt['card_type_val'] = gd_cardtype_cnt['card_type'].map(cardtype_dict)
    gd_cardtype_cnt = gd_cardtype_cnt[['date','time','cardtype_cnt','card_type_val']]
    gd_cardtype_cnt_group = gd_cardtype_cnt.groupby(['date','time','card_type_val'])['cardtype_cnt'].sum()
    line_count_file = './data/count/final_%s_count.txt'%line
    line_count = pd.read_csv(line_count_file,header=None)
    line_count.columns=['date','time','count']
    print gd_cardtype_cnt.columns
    gd_cardtype0_cnt = gd_cardtype_cnt[gd_cardtype_cnt['card_type_val']==0]
    gd_cardtype0_cnt.columns = ['date','time','cardtype0_cnt','0']
    gd_cardtype1_cnt = gd_cardtype_cnt[gd_cardtype_cnt['card_type_val']==1]
    gd_cardtype1_cnt.columns = ['date','time','cardtype1_cnt','1']
    gd_cardtype2_cnt = gd_cardtype_cnt[gd_cardtype_cnt['card_type_val']==2]
    gd_cardtype2_cnt.columns = ['date','time','cardtype2_cnt','2']
    gd_cardtype3_cnt = gd_cardtype_cnt[gd_cardtype_cnt['card_type_val']==3]
    gd_cardtype3_cnt.columns = ['date','time','cardtype3_cnt','3']

    gd_cardtype4_cnt = gd_cardtype_cnt[gd_cardtype_cnt['card_type_val']==4]
    gd_cardtype4_cnt.columns = ['date','time','cardtype4_cnt','4']

    gd_cardtype5_cnt = gd_cardtype_cnt[gd_cardtype_cnt['card_type_val']==5]
    gd_cardtype5_cnt.columns = ['date','time','cardtype5_cnt','5']

    gd_cardtype6_cnt = gd_cardtype_cnt[gd_cardtype_cnt['card_type_val']==6]
    gd_cardtype6_cnt.columns = ['date','time','cardtype6_cnt','6']
    line_count_weight = pd.merge(line_count,gd_cardtype0_cnt,how='left',on=['date','time'])
    line_count_weight = pd.merge(line_count_weight,gd_cardtype1_cnt,how='left',on=['date','time'])
    line_count_weight = pd.merge(line_count_weight,gd_cardtype2_cnt,how='left',on=['date','time'])
    line_count_weight = pd.merge(line_count_weight,gd_cardtype3_cnt,how='left',on=['date','time'])
    line_count_weight = pd.merge(line_count_weight,gd_cardtype4_cnt,how='left',on=['date','time'])
    line_count_weight = pd.merge(line_count_weight,gd_cardtype5_cnt,how='left',on=['date','time'])
    line_count_weight = pd.merge(line_count_weight,gd_cardtype6_cnt,how='left',on=['date','time'])
    line_count_weight = line_count_weight.fillna(value=0)
    line_count_weight['cardtype0_weight'] = line_count_weight['cardtype0_cnt']/(1.0*line_count_weight['count'])
    line_count_weight['cardtype1_weight'] = line_count_weight['cardtype1_cnt']/(1.0*line_count_weight['count'])
    line_count_weight['cardtype2_weight'] = line_count_weight['cardtype2_cnt']/(1.0*line_count_weight['count'])
    line_count_weight['cardtype3_weight'] = line_count_weight['cardtype3_cnt']/(1.0*line_count_weight['count'])
    line_count_weight['cardtype4_weight'] = line_count_weight['cardtype4_cnt']/(1.0*line_count_weight['count'])
    line_count_weight['cardtype5_weight'] = line_count_weight['cardtype5_cnt']/(1.0*line_count_weight['count'])
    line_count_weight['cardtype6_weight'] = line_count_weight['cardtype6_cnt']/(1.0*line_count_weight['count'])
    line_count_weight = line_count_weight[['date','time','cardtype0_weight','cardtype1_weight','cardtype2_weight','cardtype3_weight',
                                          'cardtype4_weight','cardtype5_weight','cardtype6_weight']]
    print line_count_weight.head()
    # join and compute the weight
    cardtype_name = './data/cardtype_%s_count_weight.txt'%line
    line_count_weight.to_csv(cardtype_name,header=True,index=False)
