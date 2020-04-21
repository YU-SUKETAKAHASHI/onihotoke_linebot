import psycopg2
import psycopg2.extras
import os


class DataBase:        
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')
        self.connect()

    def connect(self):
        self.connection = psycopg2.connect(self.database_url)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def get_info_list(sql):
        self.cursor.execute (sql)
        results = self.cursor.fetchall()
        return results

    def execute_sql(sql):
        self.cursor.execute (sql)


# ユーザ情報を管理するクラス
class User_DB(DataBase):

    # 渡されたuseridをDBから削除する
    def del_userinfo(self, userid):
        sql_delete = f"delete from user_info where userid='{userid}'"
        self.execute_sql(sql_delete)

    # 渡されたユーザ情報をDBに登録する
    def add_userinfo(self, major, userid):
        sql_add = f"insert into user_info (major, userid) values ('{major}', '{userid}')"
        self.execute_sql(sql_add)

    # 渡されたuseridのdepartmentを返却
    def get_usermajor(userid):
        sql_search = f"select major from user_info where userid='{userid}'"
        user_major = self.get_info_list(sql_search)
        if not user_major:
            return False
        return user_major[0][0]


# シラバス情報を管理するDB
class Syllabus_DB(DataBase):

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
            lecture_info = self.get_info_list(sql)

            if class_=="機知" or class_=="情物" or class_=="化バイ" or class_=="材料" or class_=="建築":
                sql = f"select * from lecture_info where group_='外国語' and classes like '%工%' and semester like '%1Q%'"
                lecture_info_ = self.get_info_list(sql)
                lecture_info.extend(lecture_info_)

        else:    
            sql = f"select * from lecture_info where group_='{group}' and classes like '%{class_}%' "
            lecture_info = self.get_info_list(sql)

            if class_=="機知" or class_=="情物" or class_=="化バイ" or class_=="材料" or class_=="建築":
                sql = f"select * from lecture_info where group_='{group}' and classes like '%工%' "
                lecture_info_ = self.get_info_list(sql)
                lecture_info.extend(lecture_info_)

        return lecture_info

    
class Onihotoke_DB(DataBase):
    def __init__(self):
        self.keys = ["subject", "teacher", "difficulty", "worth",
                            "comment", "test", "report", "attendance", "post date"]

    #講義名を受け取り,その講義を担当している教授名を返す.
    def searchTeacher(text, bool):
        text = neologdn.normalize(text)#正規化
        text = text.split("，")[0] if "，" in text else text
        text = text.replace(" ", "")
        text = text.replace("C1", "")

        sql_lecture = f"select * from lecture_assessments where subject LIKE '%{text}%'"
        lecture_info = self.get_info_list(sql_lecture)#検索結果が入っている.

        teacher_info_list = []
        if bool:
            #[{'subject': '実践機械学習', 'teacher': '篠原歩', 'difficulty': '仏', 'worth': '', 'comment': 'Pythonに関する授業',
            # 'test': '', 'report': '', 'attendance': ''},
            # {'subject': '実践機械学習', 'teacher': '篠原歩', 'difficulty': '仏', 'worth': '', 'comment': '機械学習に興味があるけどよく知らないという人にはよさそう',
            # 'test': '', 'report': 'あり', 'attendance': 'あり'}]　こういう辞書のリストをつくる
            teacher_info_list = [{key:value for key, value in zip(self.keys, _lecture_info)} for _lecture_info in lecture_info]
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
        lecture_info = self.get_info_list(sql_lecture)#検索結果が入っている

        lecture_info_list = []
        if bool:
            lecture_info_list = [{key:value for key, value in zip(self.keys, _lecture_info)} for _lecture_info in lecture_info]
        else:
            if lecture_info:
                lecture_info_list = list(set([_lecture_info[0] for _lecture_info in lecture_info]))#教授名だけのリスト.
                if lecture_info_list[0]=="":
                    lecture_info_list = lecture_info_list[1:]

        return lecture_info_list