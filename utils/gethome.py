from utils import *
from utils.util import df, typeList


def getHomeData():
    print("最值!!")
    maxRate = df['评分'].max()
    castsList = typeList('演员')
    filtered_castsList = [cast for cast in castsList if cast]
    maxCasts = max(filtered_castsList,key=filtered_castsList.count) # 出场最多演员
    countryList = typeList('拍摄国家')
    filtered_countryList = [country for country in countryList if country and country != '/']

    maxCountry = max(filtered_countryList, key=filtered_countryList.count)  # 出场最多国家
    typelist = typeList('电影类型')
    lenType = len(set(typelist))
    maxType = max(typelist, key=typelist.count)  # 最多的电影类型，按照在列表中出现的次数来比较
    return lenType,maxRate, maxCasts,maxCountry


# 定义函数 getTypeEcharData，用于处理电影类型数据
def getTypeEcharData():
    # 获取电影类型列表
    typelist = typeList('电影类型')
    typeobj = {}
    print('---------------------------')
    print(typelist)
    for types in typelist:
        # 分割每个单元格中的多个类型为独立的类型
        splitted_types = types.split()
        for type_ in splitted_types:
            if typeobj.get(type_, -1) == -1:
                typeobj[type_] = 1
            else:
                typeobj[type_] += 1

    typeEcharData = []
    # 更改数据类型
    for key, item in typeobj.items():
        typeEcharData.append({
            'name': key,
            'value': item
        })
    print(typeEcharData)
    # 返回包含类型及其出现次数对象的列表
    return typeEcharData


# 定义函数 getRateEcharData 用于获取评分数据并进行统计
def getRateEcharData():
    # 打印信息，用于调试
    print("最评分")

    # 获取评分列表，并将评分转换为浮点数类型
    ratelist = df['评分'].map(lambda x: float(x)).values
    # 对评分列表进行排序
    ratelist.sort()
    # 初始化空字典用于存储评分统计结果
    rateObj = {}

    # 统计每个评分的数量
    for i in ratelist:
        if rateObj.get(i, -1) == -1:
            rateObj[i] = 1
        else:
            rateObj[i] += 1
    # 返回评分列表和对应数量的列表
    return list(rateObj.keys()), list(rateObj.values())


# 返回数据库中的全部数据
def getTableData():
    return df.values

getHomeData()
