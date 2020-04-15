#旧鬼仏表の全講義データをスクレイピングしてきてDataFrameに固めて、データベースにインサートする

#%%
from urllib.error import HTTPError  # HTTPのエラーを抽出
from urllib.error import URLError  # URLのエラーを抽出
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import re
from extract_review_id import ids
import pandas as pd
from sqlalchemy import create_engine
import neologdn
from time import sleep
import os


url_1= "https://www.kibutu.com/search2.php?number="
url_2 = "&university=tohoku"

print(len(ids))

describes = []
for id_num in ids:
    full_url = url_1 + id_num + url_2
    html_file = urlopen(full_url)
    soup = bs(html_file, "html.parser")
    tables = soup.find_all("table")
    # print(tables[len(tables)-1])
    #print(tables)
    describes.append(tables[len(tables)-1] if tables else "")#後ろから２番目のtableがお目当て
    print(id_num," done~")
    # sleep(0.1)

#print("1==================================================")

parsed = [str(each).split("</font>") for each in describes]#tableが一続きの要素になっているのでfontで分割する
#print("2==================================================-")

limited = [[each[2*n+1] for n in range(int(len(each)/2))] for each in parsed ]#凡例を取り除き、値だけを抽出

#print("3==================================================-")

completed = []
for each in limited:
    _limited = []
    sorted = []
    #print(each)
    for _each in each:
        # gotten = re.search(r"(?<=>)\w+",_each)#日本語部分だけ抽出
        # gotten = gotten.group(0) if gotten else ""#日本語部分だけ抽出

        #正規表現でうまくcommentを取得できなかったため24文字目以降を取得するかたちに変更
        gotten = _each[24:]
        gotten = neologdn.normalize(gotten)
        _limited.append(gotten)
    _limited.append("")#worthに対応する""を追加（旧鬼仏表のため空欄）
    sorted.append(_limited[1])#出力に合わせてソートする
    sorted.append(_limited[0])
    sorted.append(_limited[4])
    sorted.append(_limited[9])
    sorted.append(_limited[8])
    sorted.append(_limited[5])
    sorted.append(_limited[6])
    sorted.append(_limited[7])
    sorted.append(_limited[3])
    completed.append(sorted)

#print("4==================================================-")


columns = [
          "subject",
          "teacher",
          "difficulty",
          "worth",
          "comment",
          "test",
          "report",
          "attendance",
          "posted date"
          ]

df_completed = pd.DataFrame(completed, columns=columns)



#heroku postgresにテーブルを作成
print("now inserting")
# DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine("postgres://iyclxsbznyhojl:1f5ec245d0bbf4bf5e58204da1ef0b172f971c102efe38fad8a1e36699a19974@ec2-18-210-51-239.compute-1.amazonaws.com:5432/de9fvgtnehbuju")
df_completed.to_sql("lecture_assessments", engine, if_exists="replace", index=False)

print("completed")
