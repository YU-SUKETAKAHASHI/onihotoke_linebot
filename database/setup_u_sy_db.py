import pandas as pd
from sqlalchemy import create_engine
import os


def gen_lecture_info_db():
    # DATABASE_URL = os.environ["DATABASE_URL"]
    db_1 = pd.read_csv("kamoku_r02_0310.csv", encoding="cp932")
    db_2 = pd.read_csv("kamoku_r02_0311.csv", encoding="cp932")
    db_3 = pd.read_csv("kamoku_r02_0312.csv", encoding="cp932")
    try:
        engine = create_engine("postgres://dqsbtephjgsmln:c628c0fcd1b92616b0e98e990e26eba3d016646e7acd8c043f37d16829880d8e@ec2-3-213-192-58.compute-1.amazonaws.com:5432/dd0svg9d904uaa")
        db_1.to_sql("lecture_info", engine, if_exists="replace", index=False)
        db_2.to_sql("lecture_info", engine, if_exists="append", index=False)
        db_3.to_sql("lecture_info", engine, if_exists="append", index=False)
        print("success")
    except:
        print("faild")


def gen_user_info_db():
    # DATABASE_URL = os.environ["DATABASE_URL"]
    data = {"major": ["学部"],
            "userid": ["1234567890"]}
    userid_df = pd.DataFrame(data)
    try:
        engine = create_engine("postgres://dqsbtephjgsmln:c628c0fcd1b92616b0e98e990e26eba3d016646e7acd8c043f37d16829880d8e@ec2-3-213-192-58.compute-1.amazonaws.com:5432/dd0svg9d904uaa")
        userid_df.to_sql("user_info", engine, if_exists="replace", index=False)
        print("success")
    except:
        print("faild")


if __name__ == "__main__":
    gen_lecture_info_db()
    gen_user_info_db()

