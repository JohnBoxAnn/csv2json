# -*-coding:utf-8 -*-
import pandas as pd
import math

def ValuesWeight(Attr):
    df = pd.read_csv('./data/Accidents0515.csv')
    # 取出指定属性分析以及标签 Accident_Severity
    df1 = df[[Attr, "Accident_Severity"]]
    # 列表存储属性的不同取值
    list = df1[Attr].unique()
    # 常量存储行数
    AccidentNum = df1.shape[0]
    # dataframe 转化为矩阵操作
    matix = df1.values
    # list1里存放事故等级为1的属性不同取值个数，list2为等级2，list3为等级3
    list1 = [0]*len(list)
    list2 = [0]*len(list)
    list3 = [0]*len(list)
    # 将属性的不同取值在不同受伤等级的个数存储到相应列表中
    for i in range(AccidentNum):
        for j in range(len(list)):
            if matix[i][0] == list[j]:
                if matix[i][1] == 1:
                    list1[j] = list1[j] + 1
                elif matix[i][1] == 2:
                    list2[j] = list2[j] + 1
                elif matix[i][1] == 3:
                    list3[j] = list3[j] + 1
    CountList = [list1, list2, list3]
    print(Attr+"属性的不同取值在不同受伤等级的个数列表", CountList)
    # 定义事故等级权重
    A = math.log(AccidentNum/sum(list1),2)
    B = math.log(AccidentNum/sum(list2),2)
    C = math.log(AccidentNum/sum(list3),2)
    Degree1 = A/(A+B+C)
    Degree2 = B/(A+B+C)
    Degree3 = C/(A+B+C)
    print("D1:%f, D2:%f, D3:%f"%(Degree1, Degree2, Degree3))
    # 构造权重列表，存储属性每个取值的权重
    ValuesWeight = [0]*len(list)
    for i in range(len(list)):
        de = list1[i]+list2[i]+list3[i]
        ValuesWeight[i] = (list1[i]/de)*Degree1 + (list2[i]/de)*Degree2 + (list3[i]/de)*Degree3
    print(Attr+"各个取值", list)
    print(Attr+"各个取值权重", ValuesWeight)
    # 属性权重系数，系数越大对事故影响等级越高
    AttrWeight = sum(ValuesWeight)
    print(Attr+"权重系数", AttrWeight)
    print("-------------------------------------------------")
    print("          开始计算下一个属性的权重")
    print("-------------------------------------------------")

if __name__ == '__main__':
    AttrList = ["Day_of_Week", "Road_Type", "1st_Road_Class", "Time", "Speed_limit", "Junction_Detail",
                "Junction_Control", "Light_Conditions", "Urban_or_Rural_Area"]
    ValuesWeight(AttrList[0])
    ValuesWeight(AttrList[1])
    ValuesWeight(AttrList[2])
    ValuesWeight(AttrList[4])
    ValuesWeight(AttrList[5])
    ValuesWeight(AttrList[6])
    ValuesWeight(AttrList[7])
    ValuesWeight(AttrList[8])