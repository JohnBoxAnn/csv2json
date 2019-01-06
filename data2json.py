# -*-coding:utf-8 -*-
import json
import pandas as pd
import os
import csv
import numpy as np
#from pyecharts import Map, Geo


# 获取文件的路径
def get_data_path(file_name):
    path = os.getcwd()#获得当前工作区路径
    path = os.path.join(path,"data")#要把数据放在./data/里
    data_path = os.path.join(path, file_name)
    return data_path

def get_target_path(file_name):
    path = os.getcwd()
    path = os.path.join(path,"json")#输出在./json/里
    target_path = os.path.join(path, file_name)
    return target_path

def count_to_json(data_file,target_file):
    # 读取文件
    read_data = pd.read_csv(get_data_path(data_file))
    target_path = get_target_path(target_file)
    # 属性名称
    attr = ["Longitude","Latitude","Accident_Severity","Date","Time","Day_of_Week"]
    # 临时字典
    tempdict = {}
    
    Longitude = read_data[attr[0]]
    Latitude = read_data[attr[1]]
    AcSev = read_data[attr[2]]
    Date = pd.to_datetime(read_data[attr[3]])
    Time = read_data[attr[4]]
    Week = read_data[attr[5]]
    print("Data Reading Finished")

    for i in range(1, len(Longitude)):
        if (str(Date[i])[:7] in tempdict):
            if str(Longitude[i])+','+str(Latitude[i]) in tempdict[str(Date[i])[:7]]:
                tempdict[str(Date[i])[:7]][str(Longitude[i])+','+str(Latitude[i])] = tempdict[str(Date[i])[:7]][str(Longitude[i])+','+str(Latitude[i])] + 1
            else:
                tempdict[str(Date[i])[:7]][str(Longitude[i])+','+str(Latitude[i])] = 1
        else:
            tempdict[str(Date[i])[:7]] = dict()
            tempdict[str(Date[i])[:7]][str(Longitude[i])+','+str(Latitude[i])] = 1
    print("dict Finished")

    string = ""
    lN = []
    lD = []
    min = float('inf')
    max = 0
    for i in range(len(tempdict)):
        [date, subdict] = tempdict.popitem()
        if date == 'NaT':
            continue
        for j in range(len(subdict)):
            [string, count] = subdict.popitem()
            if string == "nan,nan":
                continue
            lng = float(string[0:string.find(',')])
            lat = float(string[string.find(',') + 1:])
            lN.append(dict())
            lN[-1] = dict({"location":dict(zip(["lat","lng"],[lat,lng])),"count":count})
            max = count>max and count or max
            min = count<min and count or min
        lD.append(dict())
        lD[-1] = dict({date:lN})
        lN = []
    print("lD Finished")
    print("max: %d, min: %d"%(max, min))
    tempdict.clear()

    JSON = dict({"data":lD, "max":max, "min":min, "total":len(lD)})
    fw = open(target_path, "w")
    json.dump(JSON, fw, sort_keys = False, indent = 4)
    fw.close()
    print("Write into JSON Finished")

if __name__ == '__main__':
    count_to_json("Accidents0515.csv","latlngdateM.json")
