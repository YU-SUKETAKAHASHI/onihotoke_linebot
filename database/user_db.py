import psycopg2
import psycopg2.extras
import os

# 入力されたSQL文を用いてselectを行い,指定されたユーザー情報のリストを返却する.
def get_userinfo_list(sql):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute (sql)
            results = cur.fetchall()
    return results


# 入力されたSQL文でDBを操作する
def operation_db(sql):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute (sql)


# DBと接続する
def get_connection():
    DATABASE_URL = os.environ.get('DATABASE_URL')
    return psycopg2.connect(DATABASE_URL)


# 渡されたuseridをDBから削除する
def del_userinfo(userid):
    sql_delete = f"delete from user_info where userid='{userid}'"
    operation_db(sql_delete)


# 渡されたユーザ情報をDBに登録する
def add_userinfo(major, userid):
    sql_add = f"insert into user_info (major, userid) values ('{major}', '{userid}')"
    operation_db(sql_add)


# 渡されたuseridのdepartmentを返却
def get_usermajor(userid):
    sql_search = f"select major from user_info where userid='{userid}'"
    user_major = get_userinfo_list(sql_search)
    if not user_major:
        return False
    return user_major[0][0]


if __name__ == "__main__":
    print("jobs!")
