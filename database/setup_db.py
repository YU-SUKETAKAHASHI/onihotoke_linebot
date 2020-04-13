import pandas as pd
from sqlalchemy import create_engine


# db_1 = pd.read_csv("kamoku_r02_0310.csv", encoding="cp932")
# db_2 = pd.read_csv("kamoku_r02_0311.csv", encoding="cp932")
db_3 = pd.read_csv("kamoku_r02_0312.csv", encoding="cp932")

engine = create_engine(DATABASE_URL)
# db_1.to_sql("lecture_info", engine, if_exists="append", index=False)
# db_2.to_sql("lecture_info", engine, if_exists="append", index=False)
db_3.to_sql("lecture_info", engine, if_exists="append", index=False)
print("finish!")

