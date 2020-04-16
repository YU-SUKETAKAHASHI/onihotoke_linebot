#データベースから講義データを検索する
import psycopg2
import psycopg2.extras
import os
from sqlalchemy import create_engine
import neologdn

keys = ["subject", "teacher", "difficulty", "worth", "comment", "test", "report", "attendance", "post date"]


# 入力されたSQLを用いてselectを行い,リストを返却する.
def get_dict_resultset(sql):
    # conn = get_connection()
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute (sql)
            results = cur.fetchall()
    return results


def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)


#講義名を受け取り,その講義を担当している教授名を返す.
def searchTeacher(text, bool):
    text = neologdn.normalize(text)#正規化
    text = text.split("，")[0] if "，" in text else text
    text = text.replace(" ", "")
    text = text.replace("C1", "")

    sql_lecture = f"select * from lecture_assessments where subject LIKE '%{text}%'"
    lecture_info = get_dict_resultset(sql_lecture)#検索結果が入っている.

    teacher_info_list = []
    if bool:
        #[{'subject': '実践機械学習', 'teacher': '篠原歩', 'difficulty': '仏', 'worth': '', 'comment': 'Pythonに関する授業',
        # 'test': '', 'report': '', 'attendance': ''},
        # {'subject': '実践機械学習', 'teacher': '篠原歩', 'difficulty': '仏', 'worth': '', 'comment': '機械学習に興味があるけどよく知らないという人にはよさそう',
        # 'test': '', 'report': 'あり', 'attendance': 'あり'}]　こういう辞書のリストをつくる
        teacher_info_list = [{key:value for key, value in zip(keys, _lecture_info)} for _lecture_info in lecture_info]
    else:
        if lecture_info:
            teacher_info_list = list(set([_lecture_info[1] for _lecture_info in lecture_info]))#教授名だけのリスト. 一度setにしてからlistに戻すことで,重複している要素を除いている.
            if teacher_info_list[0]=="":#先頭が空であることが多いので,それを除去.
                teacher_info_list = teacher_info_list[1:]

    return teacher_info_list


#教官名を受け取り,担当している講義名を返す
def searchLecture(text, bool):
    text = neologdn.normalize(text)
    text = text.replace(" ", "")
    text = text.replace("C1", "")
    
    sql_lecture = f"select * from lecture_assessments where teacher LIKE '%{text}%'"
    lecture_info = get_dict_resultset(sql_lecture)#検索結果が入っている

    lecture_info_list = []
    if bool:
        lecture_info_list = [{key:value for key, value in zip(keys, _lecture_info)} for _lecture_info in lecture_info]
    else:
        if lecture_info:
            lecture_info_list = list(set([_lecture_info[0] for _lecture_info in lecture_info]))#教授名だけのリスト.
            if lecture_info_list[0]=="":
                lecture_info_list = lecture_info_list[1:]

    return lecture_info_list


#講義名と教官名を受け取る.ただし順番はわからない.　★二回データベースを検索してるから効率悪い。
def searchAll(text1, text2):
    list1 = searchTeacher(text1, True)#とりあえずどっちのワードでも検索してみて,つなげてる.
    list2 = searchTeacher(text2, True)
    list1.extend(list2)#講義名でヒットした講義が格納されている.

    list3 = searchLecture(text1, True)#とりあえずどっちのワードでも検索してみて、つなげてる.
    list4 = searchLecture(text2, True)
    list3.extend(list4)#教官名でヒットした講義が格納されている.

    all_info = [lec for lec in list1 if lec in list3]#共通の要素を抽出.

    return all_info


if __name__ == "__main__":
    print("jobs")