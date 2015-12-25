#-*-coding:utf-8-*-
__author__ = 'burness'
'''
这个脚本用来处理count和bus_count文件当中的时间问题
'''
def process_deal_time(path,file_name):
    file_name_path = path+file_name
    file_name_write = path +'final_'+file_name
    with open(file_name_path) as f:
        with open(file_name_write,'w+') as f2:
            for line in f.readlines():
                if line[4] == '0' and  line[6] == '0':
                    line=line[:4]+'/'+line[5:6]+'/'+line[7:8]+','+line[8:]
                elif line[4] == '0' and line[6]!= '0':
                    line=line[:4]+'/'+line[5:6]+'/'+line[6:8]+','+line[8:]
                elif line[4] != '0' and line[6] == '0':
                    line = line[:4]+'/'+line[4:6]+'/'+line[7:8]+','+line[8:]
                else:
                    line = line[:4]+'/'+line[4:6]+'/'+line[6:8]+','+line[8:]
                f2.write(line)

process_deal_time('./data/count/','线路6_count.txt')
process_deal_time('./data/count/','线路11_count.txt')
process_deal_time('./data/bus_count/','线路6_bus_count.txt')
process_deal_time('./data/bus_count/','线路11_bus_count.txt')

