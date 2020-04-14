import pandas as pd
from sqlalchemy import create_engine


def gen_lecture_info_db():
    db_1 = pd.read_csv("kamoku_r02_0310.csv", encoding="cp932")
    db_2 = pd.read_csv("kamoku_r02_0311.csv", encoding="cp932")
    db_3 = pd.read_csv("kamoku_r02_0312.csv", encoding="cp932")

    engine = create_engine(DATABASEURL)
    db_1.to_sql("lecture_info", engine, if_exists="append", index=False)
    db_2.to_sql("lecture_info", engine, if_exists="append", index=False)
    db_3.to_sql("lecture_info", engine, if_exists="append", index=False)
    print("finish!")

def gen_user_info_db():
    data = {"department": ["学部"],
            "subject": ["学科"],
            "userid": ["1234567890"]}
    userid_df = pd.DataFrame(data)

    engine = create_engine(DATABASEURL)
    userid_df.to_sql("user_info", engine, if_exists="append", index=False)

if __name__ == "__main__":
    #gen_lecture_info_db()
    gen_user_info_db()

