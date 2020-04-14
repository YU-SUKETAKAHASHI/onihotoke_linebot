#旧鬼仏表の全講義データのURLのid部分をまとめて返す

import re

my_html = open("input/all_new.html",encoding="utf-8_sig").read()

def extract_ids():
    pattern = r'number=(.*)&amp;university'
    matchs = re.finditer(pattern, my_html)

    print("extract_idsが実行されました")
    return [match.groups()[0] for match in matchs]

ids = extract_ids()

if __name__ == "__main__":
    extract_ids()#[:3]#3件だけ

#参考
#https://qiita.com/Yuu94/items/9ffdfcb2c26d6b33792e
