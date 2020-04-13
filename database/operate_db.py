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


def search_lecture_info(group, classes):
    sql = f"select * from lecture_info where group='{group}' and classes like '%{classes}%'"
    lecture_info = get_lecture_list(sql)
    return lecture_info


# def search_society_info(classes):
#     sql = f"select * from lecture_info where (group=社会論 or group=社会科学) and classes like '%{classes}%'"
#     lecture_info = get_lecture_list(sql)
#     return lecture_info



# def search_nature_info(classes):

#     return lecture_info