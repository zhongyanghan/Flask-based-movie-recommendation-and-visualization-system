

import pandas as pd
from sqlalchemy import create_engine


df=pd.read_excel('豆瓣电影 的副本.xls')
df=df.dropna()
# 数据库配置
dbconfig = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '123456',
    'database': 'dbmovie',
    'driver': 'mysql+pymysql',  # 或 'mysql+mysqlclient'，取决于你安装的MySQL驱动
}

# 创建数据库引擎
engine = create_engine(f"{dbconfig['driver']}://{dbconfig['user']}:{dbconfig['passwd']}@{dbconfig['host']}/{dbconfig['database']}")

# 将 DataFrame 写入数据库
# 如果表不存在，它会自动创建（如果你有权限的话）
# 注意：这里的 'movie' 是你的表名
df.to_sql('movie', con=engine, if_exists='append', index=True, index_label='id')