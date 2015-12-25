#-*-coding:utf-8-*-
__author__ = 'burness'
'''
这个脚本用来处理cardtype count当中的时间问题
'''
def process_deal_time(path,file_name):
    file_name_path = path+file_name
    file_name_write = path +'final_'+file_name
    with open(file_name_path) as f:
        with open(file_name_write,'w+') as f2:
            for line in f.readlines():
                line_list = line.split(',')
                deal_time_str = line_list[1]
                if deal_time_str[4] == '0' and  deal_time_str[6] == '0':
                    deal_time_str=deal_time_str[:4]+'/'+deal_time_str[5:6]+'/'+deal_time_str[7:8]+','+deal_time_str[8:]
                elif deal_time_str[4] == '0' and deal_time_str[6]!= '0':
                    deal_time_str=deal_time_str[:4]+'/'+deal_time_str[5:6]+'/'+deal_time_str[6:8]+','+deal_time_str[8:]
                elif deal_time_str[4] != '0' and deal_time_str[6] == '0':
                    deal_time_str = deal_time_str[:4]+'/'+deal_time_str[4:6]+'/'+deal_time_str[7:8]+','+deal_time_str[8:]
                else:
                    deal_time_str = deal_time_str[:4]+'/'+deal_time_str[4:6]+'/'+deal_time_str[6:8]+','+deal_time_str[8:]
                f2.write(line_list[0]+','+deal_time_str+','+line_list[2])

process_deal_time('./data/count/','线路6_count_cardtype.txt')
process_deal_time('./data/count/','线路11_count_cardtype.txt')
# process_deal_time('./data/bus_count/','线路6_bus_count.txt')
# process_deal_time('./data/bus_count/','线路11_bus_count.txt')

