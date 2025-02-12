import psycopg2
import psycopg2.extras
import os

# DBと接続する
def get_connection():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    return psycopg2.connect(DATABASE_URL)


# 入力されたSQL文を用いてselectを行い,指定された講義情報のリストを返却する.
def get_lecture_list(sql):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute (sql)
            results = cur.fetchall()
    return results


def search_lecture_info(group, class_):
    """
    ==Parameta==
        group(str)   : 取得した講義の群（人間論とか）
        class_(str) : ユーザの所属（情物とか文とか）
    ==Return==
        辞書型の講義データのリスト
    """
    if group == "外国語":
        sql = f"select * from lecture_info where group_='外国語' and classes like '%{class_}%' and semester like '%1Q%'"
        lecture_info = get_lecture_list(sql)

        if class_=="機知" or class_=="情物" or class_=="化バイ" or class_=="材料" or class_=="建築":
            sql = f"select * from lecture_info where group_='外国語' and classes like '%工%' and semester like '%1Q%'"
            lecture_info_ = get_lecture_list(sql)
            lecture_info.extend(lecture_info_)

    else:    
        sql = f"select * from lecture_info where group_='{group}' and classes like '%{class_}%' "
        lecture_info = get_lecture_list(sql)

        if class_=="機知" or class_=="情物" or class_=="化バイ" or class_=="材料" or class_=="建築":
            sql = f"select * from lecture_info where group_='{group}' and classes like '%工%' "
            lecture_info_ = get_lecture_list(sql)
            lecture_info.extend(lecture_info_)

    return lecture_info
