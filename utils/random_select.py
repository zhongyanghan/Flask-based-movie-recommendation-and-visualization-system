from pymysql import *

conn = connect(host='localhost',user='root',password='123456',database='dbmovie',port=3306)
cursor = conn.cursor()