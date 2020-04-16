import pandas as pd
from sqlalchemy import create_engine
import os


def gen_lecture_info_db():
    # DATABASE_URL = os.environ["DATABASE_URL"]
    db_1 = pd.read_csv("kamoku_r02_0310.csv", encoding="cp932")
    db_2 = pd.read_csv("kamoku_r02_0311.csv", encoding="cp932")
    db_3 = pd.read_csv("kamoku_r02_0312.csv", encoding="cp932")
    try:
        engine = create_engine("postgres://iyclxsbznyhojl:1f5ec245d0bbf4bf5e58204da1ef0b172f971c102efe38fad8a1e36699a19974@ec2-18-210-51-239.compute-1.amazonaws.com:5432/de9fvgtnehbuju")
        db_1.to_sql("lecture_info", engine, if_exists="replace", index=False)
        db_2.to_sql("lecture_info", engine, if_exists="append", index=False)
        db_3.to_sql("lecture_info", engine, if_exists="append", index=False)
        print("success")
    except:
        print("faild")


def gen_user_info_db():
    DATABASE_URL = os.environ["DATABASE_URL"]
    data = {"major": ["学部"],
            "userid": ["1234567890"]}
    userid_df = pd.DataFrame(data)
    try:
        engine = create_engine(DATABASE_URL)
        userid_df.to_sql("user_info", engine, if_exists="replace", index=False)
        print("success")
    except:
        print("faild")


if __name__ == "__main__":
    gen_lecture_info_db()
    # gen_user_info_db()

