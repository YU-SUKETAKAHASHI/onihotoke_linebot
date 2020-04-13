#シラバスからの検索
def gen_card_syllabus(dic):

"""
  dic = {"subject":"思想と倫理の世界",
             "title":"現代における人間の探究―哲学的人間学入門",
             "teacher":"佐藤　透",
             "code":"CB21113",
             "semester":"１セメ",
             "day_time":"火１",
             "classes":"医保歯薬工" }

==Return==
    origin_json :取得したdicのデータでテンプレから変更したjsonデータ

"""


    origin_json = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "思想と倫理の世界",
        "size": "xl",
        "margin": "sm",
        "weight": "bold",
        "style": "italic"
      },
      {
        "type": "text",
        "text": "現代における人間の探究―哲学的人間学入門",
        "size": "xs"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "xs",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "teacher",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 2
              },
              {
                "type": "text",
                "text": "佐藤　透",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "semester",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 2
              },
              {
                "type": "text",
                "text": "１セメ",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "text",
                "text": "time",
                "flex": 2,
                "size": "sm",
                "color": "#aaaaaa"
              },
              {
                "type": "text",
                "text": "火１",
                "flex": 5,
                "size": "sm",
                "color": "#666666"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "text",
                "text": "class",
                "size": "sm",
                "flex": 2,
                "color": "#aaaaaa"
              },
              {
                "type": "text",
                "text": "医保歯薬工",
                "flex": 5,
                "color": "#666666",
                "size": "sm"
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "シラバス",
          "uri": "https://linecorp.com"
        }
      },
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "鬼仏",
          "uri": "https://linecorp.com"
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
  }
}

    subject = dic["subject"]
    title = dic["title"]
    teacher = dic["teacher"]
    code = dic["code"]
    semester = dic["semester"]
    day_time = dic["day_time"]
    classes = dic["classes"]


    origin_json["body"]["contents"][0]["text"] = subject
    origin_json["body"]["contents"][1]["text"] = title
    origin_json["body"]["contents"][2]["contents"][0]["contents"][1]["text"] = teacher
    origin_json["body"]["contents"][2]["contents"][1]["contents"][1]["text"] = semester
    origin_json["body"]["contents"][2]["contents"][2]["contents"][1]["text"] = day_time
    origin_json["body"]["contents"][2]["contents"][3]["contents"][1]["text"] = classes
    origin_json["footer"]["contents"][0]["action"]["uri"] = "https://craft.cite.tohoku.ac.jp/qsl/syllabus/display/" + code



    return origin_json



def gen_card_onihotoke(dic):

"""
dic = {'subject': '思想と倫理の世界',
    'teacher': '佐藤　透',
    'difficulty': '仏',
    'worth': 'あり',
    'comment': '非常に有意義でした',
    'test': 'なーい',
    'report': '重すぎます',
    'attendance': '毎回',
    'postdate':'2020年04月13日'}

==Return==
    origin_json :取得したdicのデータでテンプレから変更したjsonデータ

"""

    origin_json = {
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": " "
      }
    ],
    "backgroundColor": "#b0c4de"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "思想と倫理の世界",
        "size": "xl",
        "weight": "bold",
        "style": "italic"
      },
      {
        "type": "separator"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "teacher",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 2
              },
              {
                "type": "text",
                "text": "teacher",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "difficulty",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 2
              },
              {
                "type": "text",
                "text": "difficulty",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "worth",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 2
              },
              {
                "type": "text",
                "text": "worth",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "test",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 2
              },
              {
                "type": "text",
                "text": "test",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "report",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 2
              },
              {
                "type": "text",
                "text": "report",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "attendance",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 2
              },
              {
                "type": "text",
                "text": "attendance",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "comment",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 2
              },
              {
                "type": "text",
                "text": "comment",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "postdate",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 2
              },
              {
                "type": "text",
                "text": "postdate",
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "spacer",
        "size": "xs"
      }
    ]
  },
  "styles": {
    "header": {
      "separator": True
    }
  }
}



    #各要素を取得する
    subject = dic["subject"]
    teacher = dic["teacher"]
    difficulty = dic["difficulty"]
    worth = dic["worth"]
    test = dic["test"]
    report = dic["report"]
    attendance = dic["attendance"]
    postdate = dic["postdate"]
    comment = dic["comment"]
    #print(difficulty)


    #commentは一番最後に置きます
    origin_json["body"]["contents"][0]["text"] = subject
    origin_json["body"]["contents"][2]["contents"][0]["contents"][1]["text"] = teacher
    origin_json["body"]["contents"][2]["contents"][1]["contents"][1]["text"] = difficulty
    origin_json["body"]["contents"][2]["contents"][2]["contents"][1]["text"] = worth
    origin_json["body"]["contents"][2]["contents"][3]["contents"][1]["text"] = test
    origin_json["body"]["contents"][2]["contents"][4]["contents"][1]["text"] = report
    origin_json["body"]["contents"][2]["contents"][5]["contents"][1]["text"] = attendance
    origin_json["body"]["contents"][2]["contents"][6]["contents"][1]["text"] = postdate
    origin_json["body"]["contents"][2]["contents"][7]["contents"][1]["text"] = comment


    #difficultyに応じてヘッダーの色を変更
    if "仏" in difficulty:
        origin_json["header"]["backgroundColor"] = "#fffacd"
    elif "鬼" in difficulty:
        origin_json["header"]["backgroundColor"] = "#f08080"
    else:
        origin_json["header"]["backgroundColor"] = "#b0c4de"

    return origin_json
