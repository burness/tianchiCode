#-*-coding:utf-8-*-

with open('./data/result/2015-11-28/traffic_线路6GBDT_result.txt') as f:
    with open('./data/result/2015-11-28/final_result.txt','a') as fwrite:
        for line in f.readlines():
            tmp_list = line.strip().split(',')
            if len(tmp_list[1])==1:
                tmp_list[1] = '0'+tmp_list[1]
            line_write = tmp_list[3]+','+tmp_list[0]+','+tmp_list[1]+','+tmp_list[2]+'\n'
            fwrite.write(line_write)

with open('./data/result/2015-11-28/traffic_线路11GBDT_result.txt') as f:
    with open('./data/result/2015-11-28/final_result.txt','a') as fwrite:
        for line in f.readlines():
            tmp_list = line.strip().split(',')
            if len(tmp_list[1])==1:
                tmp_list[1] = '0'+tmp_list[1]
            line_write = tmp_list[3]+','+tmp_list[0]+','+tmp_list[1]+','+tmp_list[2]+'\n'
            fwrite.write(line_write)
