#新鬼仏表のデータベースから必要なデータだけを抽出して整理し、新しいデータベースに突っ込む
import psycopg2
import psycopg2.extras
import os
from sqlalchemy import create_engine
from neologdn import normalize
import pandas as pd
import re

#DBからDFを作成
dsn = TONPE
connection = psycopg2.connect(dsn)
df_ass = pd.read_sql(sql='select * from assessments;', con=connection)
df_lec = pd.read_sql(sql='select * from lectures;', con=connection)


df_merge = pd.merge(df_ass, df_lec, left_on="lecture_id", right_on="id" ,how="inner")   #lecture_idとidで2つのDFを結合している
df_new = df_merge.loc[[i for i in range(len(df_merge))],["subject","teacher","difficulty","worth","comment"]]   #欲しいとこだけ取り出す


#subjectとteacherを正規化
columns = ["subject","teacher"]
for column in columns:
    values = df_merge.loc[list(range(len(df_merge))),[column]].values
    df_new[column] = [normalize(value[0]) for value in values]


#bool値になっている列の要素を文字列に変換してから追加
columns = ["Test","report","attendance"]
for column in columns:
    values = df_merge.loc[list(range(len(df_merge))),[column]].values
    column = "test" if column == "Test" else column     #Testだけなぜか大文字だから微修正
    df_new[column]  = ["あり" if value else "なし" for value in values]


#投稿年月日の列を追加
post_date_values = df_merge.loc[list(range(len(df_merge))),["created_at_x"]].values  #created_at_x列の値を格納
df_new["posted date"] = [str(pdv)[2:12] for pdv in post_date_values]

print(df_new["worth"])

#heroku postgresにテーブルを作成
DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL)
df_new.to_sql("lecture_assessments", con=engine, if_exists="append", index=False)
