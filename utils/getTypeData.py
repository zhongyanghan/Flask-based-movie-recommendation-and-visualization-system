from utils import *
from utils.util import df, typeList

def getTypeData():
    print("找类型")
    # 假设typeList函数能够返回一个包含所有电影类型数据的列表，其中每个元素可能包含多个由空格分隔的类型
    typelist = typeList('电影类型')
    typeobj = {}
    print('---------------------------')
    for types in typelist:
        # 分割每个单元格中的多个类型为独立的类型
        splitted_types = types.split()
        for type_ in splitted_types:
            if typeobj.get(type_, -1) == -1:
                typeobj[type_] = 1
            else:
                typeobj[type_] += 1

    typeData = []
    # 更改数据类型
    for key, item in typeobj.items():
        typeData.append({
            'name': key,
            'value': item
        })
    return typeData