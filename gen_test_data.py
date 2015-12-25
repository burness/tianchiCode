#-*-coding:utf-8-*-
import copy
__author__ = 'burness'
with open('./data/test_data.csv') as f:
    with open('./data/test_data_final.csv','w+') as fwrite:
        for line in f.readlines():
            for i in range(6,22,1):
                tmpline =copy.deepcopy(line)
                tmpline = str(i)+','+tmpline
                fwrite.write(tmpline)

