import pandas as pd
from sqlalchemy import create_engine


db_1 = pd.read_csv("kamoku_r02_0310.csv", encoding="cp932")
db_2 = pd.read_csv("kamoku_r02_0311.csv", encoding="cp932")

engine = create_engine("postgres://iyclxsbznyhojl:1f5ec245d0bbf4bf5e58204da1ef0b172f971c102efe38fad8a1e36699a19974@ec2-18-210-51-239.compute-1.amazonaws.com:5432/de9fvgtnehbuju")
db_1.to_sql("lecture_info", engine, if_exists="append", index=False)
db_2.to_sql("lecture_info", engine, if_exists="append", index=False)
print("finish!")

