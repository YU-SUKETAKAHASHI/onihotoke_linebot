import pandas as pd
from sqlalchemy import create_engine


db_1 = pd.read_csv("kamoku_r02_0310.csv", encoding="cp932")
db_2 = pd.read_csv("kamoku_r02_0311.csv", encoding="cp932")

engine = create_engine(DATADASE_URL)
db_1.to_sql("lecture_info", engine, if_exists="append", index=False)
db_2.to_sql("lecture_info", engine, if_exists="append", index=False)
print("finish!")

