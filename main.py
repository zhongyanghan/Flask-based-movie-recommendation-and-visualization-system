import re
from flask import Flask, request, render_template, session, redirect, jsonify
from utils import query
#from utils.getHomeData import *
from utils.gethome import *
from utils.getTime_t import *
from utils.getRate_t import *
#from utils.getMapData import *
from utils.getmap import *
#from utils.getTypeData import *
from utils.gettype import *
from utils.getActDir_t import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pymysql import *
import pandas as pd
import json
import os
import random
import requests

app = Flask(__name__)
app.secret_key = 'This is session_key.'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        request.form = dict(request.form)

        def filter_fn(item):
            return request.form['email'] in item and request.form['password'] in item

        user = query.querys('select * from user', [], 'select')
        filter_user = list(filter(filter_fn, user))
        if len(filter_user):
            session['email'] = request.form['email']
            return redirect('/home')
        else:
            return render_template('error.html', message='邮箱或密码错误')


@app.before_request
def before_request():
    pat = re.compile(r'^/static')
    if re.search(pat, request.path):
        return
    if request.path == '/login':
        return
    if request.path == '/register':
        return
    email = session.get('email')
    if email:
        return None
    return redirect('/login')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/login')


@app.route('/time_t', methods=['GET', 'POST'])
def time_t():
    email = session.get('email')
    row, columns = getYearData()
    return render_template(
        'time_t.html',
        email=email,
        row=row,
        columns=columns,
    )


@app.route('/rate_t/<type>', methods=['GET', 'POST'])
@app.route('/rate_t', methods=['GET', 'POST'])
def rate_t(type='all'):
    email = session.get('email')
    typeEcharData = []
    typeList = getAllTypes()
    row, columns, typeEcharData = getAllRateDatabyType(type)

    return render_template(
        'rate_t.html',
        email=email,
        typeList=typeList,
        type=type,
        row=row,
        columns=columns,
        typeEcharData=typeEcharData,
    )


@app.route('/map_t', methods=['GET', 'POST'])
def map_t():
    print("map!!")
    email = session.get('email')
    row, columns = getMapData()
    print(row)
    print(columns)
    return render_template(
        'map_t.html',
        email=email,
        row=row,
        columns=columns,
    )

@app.route('/type_t', methods=['GET', 'POST'])
def type_t():
    print("type!!")
    email = session.get('email')
    typesData = getTypeData()
    return render_template(
        'type_t.html',
        email=email,
        typesData = typesData
    )
@app.route('/ci_yun_t', methods=['GET', 'POST'])
def ci_yun_t():
    email = session.get('email')
    image_file = 'picture/wordcloud.png'
    return render_template('ci_yun_t.html',email=email,image_file=image_file)
@app.route('/re_li_t', methods=['GET', 'POST'])
def re_li_t():
    email = session.get('email')
    image_file = 'picture/corr.png'
    return render_template('re_li_t.html',email=email,image_file=image_file)
@app.route('/act_dir_t', methods=['GET', 'POST'])
def act_dir_t():
    email = session.get('email')
    row, columns,dirs = getDirData20()
    print(dirs)

    act_row,act_columns,acts = getActData20()
    print(acts)
    return render_template(
        'act_dir_t.html',
        email=email,
        row = row,
        columns = columns,
        dirs=dirs,
        act_row = act_row,
        act_columns = act_columns,
        acts=acts,
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        print(request.form)
        request.form = dict(request.form)
        if request.form['password'] != request.form['confirm_password']:
            return render_template('error.html', message='两次密码不符合')

        def filter_fn(item):
            return request.form['email'] in item

        users = query.querys('select * from user', [], 'select')
        filter_list = list(filter(filter_fn, users))
        if len(filter_list):
            return render_template('error.html', message='该用户已被注册')
        else:
            query.querys('insert into user(username,email,password) values(%s,%s,%s)',
                         [request.form['username'], request.form['email'], request.form['password']])
            session['username'] = request.form['username']
            return redirect('/login')


@app.route('/movieList', methods=['GET', 'POST'])
def movieList():
    email = session.get('email')
    lenType, maxRate, maxCasts, maxCountry = getHomeData()
    typeEcharData = getTypeEcharData()
    row, columns = getRateEcharData()
    tableData = getTableData()
    return render_template(
        'movieList.html',
        email=email,
        lenType=lenType,
        maxRate=maxRate,
        maxCasts=maxCasts,
        maxCountry=maxCountry,
        typeEcharData=typeEcharData,
        row=row,
        columns=columns,
        tableData=tableData
    )


conn = connect(host='localhost', user='root', password='123456', database='dbmovie', port=3306, charset='utf8')
cursor = conn.cursor()


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # 获取用户选择的类型，国家和评分

        type = request.form.get("电影类型")
        country = request.form.get("电影国家")
        rating = request.form.get("最低评分")
        # 构造SQL语句，根据用户的选择筛选电影
        sql = "SELECT * FROM movie WHERE 1=1"  # 1=1是为了方便拼接条件
        # 如果用户选择了类型，添加类型条件
        if (type == "电影类型") and (country == "电影国家") and (rating == "最低评分"):
            sel = "您没有选择，随机生成的电影是："
            index = random.randint(1, 250)
            # 定义查询数据的SQL语句，根据电影的序号，从数据库中查询对应的电影信息
            sql = "SELECT * FROM movie WHERE id = %s;"
            # 执行SQL语句
            cursor.execute(sql, (index,))
            # 获取查询结果
            movie = cursor.fetchone()
            movie = (sel,) + movie[1:]
        else:
            sel = "您的选择是："
            if type != "电影类型":
                sel+= type
                sql += " AND 电影类型 LIKE '%{}%'".format(type)
            # 如果用户选择了国家，添加国家条件
            if country != "电影国家":
                sel += country
                sql += " AND 拍摄国家 LIKE '%{}%'".format(country)
            # 如果用户选择了评分，添加评分条件
            if rating != "最低评分":
                if rating == "无下限":
                    sel += "无下限"
                    lower = 0
                else:
                    sel += rating + "分"
                    lower = float(rating)
                upper = 10
                # 拼接SQL语句，根据电影评分查询
                sql += " AND 评分 BETWEEN {} AND {}".format(lower, upper)
            insert_sql = '''
            INSERT INTO history (type, country) 
            VALUES (%s, %s)
            '''
            # 执行 SQL 语句，传入参数
            cursor.execute(insert_sql, (type, country))
            conn.commit()
            # 执行SQL语句，获取查询结果
            cursor.execute(sql)
            results = cursor.fetchall()
            if results == ():
                index = random.randint(1, 250)
                # 定义查询数据的SQL语句，根据电影的序号，从数据库中查询对应的电影信息
                sql = "SELECT * FROM movie WHERE id = %s;"
                # 执行SQL语句
                cursor.execute(sql, (index,))
                # 获取查询结果
                movie = cursor.fetchone()
                # print(isinstance(movie[0], str))
                sel += "  没有符合条件的电影哦，不如看看它吧！"
                movie = (sel,) + movie[1:]
            else:
                # 如果有符合条件的电影，随机选择一部
                movie = random.choice(results)
                movie = (sel,) + movie[1:]
        resp = requests.get(movie[2])
        data = requests.get(movie[2]).content
        with open("static/picture/image.jpg", "wb") as f:
            f.write(data)
        # 获取图片的本地绝对路径
        path = os.path.abspath("static/picture/image.jpg")
        return render_template('home.html', result=movie)
    email = session.get('email')
    print(email)
    typeEcharData = getTypeEcharData()
    row, columns = getRateEcharData()
    tableData = getTableData()
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type TEXT,
        country TEXT
    )
    '''
    # 执行 SQL 语句
    cursor.execute(create_table_sql)

    # 提交事务
    conn.commit()
    try:
        query = "SELECT * FROM history"
        # 使用 pandas 的 read_sql_query 函数执行 SQL 查询并将结果存储到 DataFrame
        df_my = pd.read_sql_query(query, conn)
        # print(df_my)
        df_my=df_my[['type','country']]

        # 显示 DataFrame 的前几行，以验证数据已成功加载
        query = "SELECT * FROM movie"
        # 使用 pandas 的 read_sql_query 函数执行 SQL 查询并将结果存储到 DataFrame
        df_movies = pd.read_sql_query(query, conn)
        # print(df_movies)
        df_movies = df_movies[['id','电影类型','拍摄国家']]


        # 合并“电影类型”和“拍摄国家”列为一个单独的特征
        df_my['特征'] = df_my['type'] + " " + df_my['country']
        df_movies['特征'] = df_movies['电影类型'] + " " + df_movies['拍摄国家']

        # 创建CountVectorizer，以转换文本特征为向量
        vectorizer = CountVectorizer()
        vectorizer.fit(pd.concat([df_my['特征'], df_movies['特征']]))

        # 转换用户记录和电影数据
        user_records_vec = vectorizer.transform(df_my['特征'])
        movies_data_vec = vectorizer.transform(df_movies['特征'])

        # 计算余弦相似度
        similarity = cosine_similarity(user_records_vec, movies_data_vec)
        print(similarity)
        # 找到最相似的电影ID
        recommended_movie_ids = similarity.mean(axis=0).argsort()[::-1][:5]  # 取平均相似度最高的5部电影
        recommended_movie_ids_indices = [df_movies['id'][i] for i in recommended_movie_ids]


        # 编写查询语句
        sql = "SELECT * FROM movie WHERE id = "+str(recommended_movie_ids_indices[0])
    except:
        sql = "SELECT * FROM movie WHERE id = 0"
    # 执行查询语句
    cursor.execute(sql)
    # 获取查询结果
    result = cursor.fetchone()
    resp = requests.get(result[2])
    data = requests.get(result[2]).content
    with open("static/picture/image.jpg", "wb") as f:
        f.write(data)
    # 获取图片的本地绝对路径
    path = os.path.abspath("static/picture/image.jpg")
    return render_template(
        'home.html',
        email=email,
        typeEcharData=typeEcharData,
        row=row,
        columns=columns,
        tableData=tableData,
        result=result,
    )

@app.route('/')
def allRequest():
    return redirect('/login')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
