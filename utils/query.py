from pymysql import *

conn = connect(host='localhost',user='root',password='123456',database='dbmovie',port=3306, charset='utf8')
cursor = conn.cursor()

def querys(sql,params,type='no_select'):
    params = tuple(params)
    cursor.execute(sql,params)
    if type != 'no_select':
        data_list = cursor.fetchall()
        conn.commit()
        return data_list
    else:
        conn.commit()
        return '数据库语句执行成功'
