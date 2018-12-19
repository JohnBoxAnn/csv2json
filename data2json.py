# -*-coding:utf-8 -*-
import json
import pandas as pd
import os
import csv
import numpy as np
#from pyecharts import Map, Geo


# 获取文件的路径
def get_path(file_name):
    path = os.getcwd()#获得当前工作区路径
    path = os.path.join(path,"data")#要把数据放在./data/里
    data_path = os.path.join(path, file_name)
    return data_path

#def csv_to_json(csv_file,json_file):
#    fo = open(csv_file, "r")  # 打开csv文件
#    ls = []
#    for line in fo:
#        line = line.replace("\n", "")  # 将换行换成空
#        ls.append(line.split(","))  # 以，为分隔符
#    fo.close()  # 关闭文件流
#    fw = open(json_file, "w")  # 打开json文件
#    for i in range(1, len(ls)):  # 遍历文件的每一行内容，除了列名
#        ls[i] = dict(zip(ls[0], ls[i]))  # ls[0]为列名，所以为key,ls[i]为value,
#        # zip()是一个内置函数，将两个长度相同的列表组合成一个关系对
#    json.dump(ls[1:], fw, sort_keys=True, indent=4)
#    # 将Python数据类型转换成json格式，编码过程
#    # 默认是顺序存放，sort_keys是对字典元素按照key进行排序
#    # indet参数用语增加数据缩进，使文件更具有可读性
#    fw.close()

def count_to_json(target_file):
    # 读取文件
    read_data = pd.read_csv(get_path(target_file))
    # 属性名称
    attr = ["Longitude","Latitude","Accident_Severity","Number_of_Casualties","Date","Time"]
    # 临时字典
    tempdict = {}
    
    Longitude = read_data[attr[0]]
    Latitude = read_data[attr[1]]
    AcSev = read_data[attr[2]]
    NoCs = read_data[attr[3]]
    Date = read_data[attr[4]]
    Time = read_data[attr[5]]
    print("Data Reading Finished")
    #for i in range(1, len(Longitude)):
    #    if str(Longitude[i])+','+str(Latitude[i]) in tempdict:
    #        tempdict[str(Longitude[i])+','+str(Latitude[i])] = tempdict[str(Longitude[i])+','+str(Latitude[i])] + 1
    #    else:
    #        tempdict[str(Longitude[i])+','+str(Latitude[i])] = 1
    #print("dict Finished")

    #string = ""
    #lc = []
    #min = float('inf')
    #max = 0
    #for i in range(len(tempdict)):
    #    try:
    #        [string, count] = tempdict.popitem()
    #    except KeyError:
    #        break
    #    if string == "nan,nan":
    #        continue
    #    long = float(string[0:string.find(',')])
    #    lat = float(string[string.find(',') + 1:])
    #    lc.append(dict())
    #    lc[-1] = dict(zip(["lat", "lng", "count"], [lat, long, count]))
    #    max = count>max and count or max
    #    min = count<min and count or min
    #print("lc Finished")
    #print("max: %d, min: %d"%(max, min))
    #tempdict.clear()

    #fw = open("latlngcount.json", "w")  # 打开json文件
    #json.dump(lc, fw, sort_keys = False, indent = 4)
    #fw.close()

    for i in range(1, len(Longitude)):
        if (AcSev[i] == 1):
            if str(Longitude[i])+','+str(Latitude[i]) in tempdict:
                tempdict[str(Longitude[i])+','+str(Latitude[i])] = tempdict[str(Longitude[i])+','+str(Latitude[i])] + int(NoCs[i])
            else:
                tempdict[str(Longitude[i])+','+str(Latitude[i])] = int(NoCs[i])
    print("dict Finished")

    string = ""
    lN = []
    min = float('inf')
    max = 0
    for i in range(len(tempdict)):
        try:
            [string, count] = tempdict.popitem()
        except KeyError:
            break
        if string == "nan,nan":
            continue
        long = float(string[0:string.find(',')])
        lat = float(string[string.find(',') + 1:])
        lN.append(dict())
        lN[-1] = dict(zip(["lat", "lng", "count"], [lat, long, count]))
        max = count>max and count or max
        min = count<min and count or min
    print("lN Finished")
    print("max: %d, min: %d"%(max, min))
    tempdict.clear()

    lN = json.dumps(lN, sort_keys = False)

    JSON = [{},{},{},{}]
    JSON[0] = dict({"data":lN})
    JSON[1] = dict({"max":max})
    JSON[2] = dict({"min":min})
    JSON[3] = dict({"total":len(lN)})
    fw = open("latlngNoCs_AcSer_1.json", "w")
    json.dump(JSON, fw, sort_keys = False, indent = 4)
    fw.close()



    #fw = open("latlngTime.json", "w")
    #json.dump(lT, fw, sort_keys = False, indent = 4)
    #fw.close()

    #tempo_data = pd.read_csv("count.csv",names=[data[i],"number"])
    #tempo_data.to_csv("count.csv",index=False)
    #csv_to_json("count.csv","{}.json".format(data[i]))

if __name__ == '__main__':
    count_to_json("Accidents0515.csv")



