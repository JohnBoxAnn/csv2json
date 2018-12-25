# -*-coding:utf-8 -*-
import pandas as pd
import math

if __name__ == '__main__':
    df = pd.read_csv('./data/Accidents0515.csv')
    # 取出指定属性分析以及标签 Accident_Severity
    df1 = df[["Day_of_Week", "Accident_Severity"]]
    # 列表存储属性的不同取值
    list = df1["Day_of_Week"].unique()
    # 常量存储行数
    AccidentNum = df1.shape[0]
    # dataframe 转化为矩阵操作
    matix = df1.values
    # 初始化列表函数
    def InitList(lists):
        for i in range(len(list)):
            lists[i] = 0
        return lists
    # list1里存放事故等级为1的属性不同取值个数，list2为等级2，list3为等级3
    list1 = [0,0,0,0,0,0,0]
    list2 = [0,0,0,0,0,0,0]
    list3 = [0,0,0,0,0,0,0]
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
    print(CountList)
    # 定义事故等级权重
    A = math.log(AccidentNum/sum(list1),2)
    B = math.log(AccidentNum/sum(list2),2)
    C = math.log(AccidentNum/sum(list3),2)
    Degree1 = A/(A+B+C)
    Degree2 = B/(A+B+C)
    Degree3 = C/(A+B+C)
    print("D1:%f, D2:%f, D3:%f"%(Degree1,Degree2,Degree3))
    # 构造权重列表，存储属性每个取值的权重
    ValuesWeight = [0,0,0,0,0,0,0]
    for i in range(len(list)):
        de = list1[i]+list2[i]+list3[i]
        ValuesWeight[i] = (list1[i]/de)*Degree1 + (list2[i]/de)*Degree2 + (list3[i]/de)*Degree3
    print("星期", list)
    print("属性各个取值权重", ValuesWeight)
    # 属性权重系数，系数越大对事故影响等级越高
    AttrWeight = sum(ValuesWeight)
    print("属性权重系数", AttrWeight)

# s1 = sum(list1)
# s2 = sum(list2)
# s3 = sum(list3)
# print(s1+s2+s3)，值等于AccidentNum
