#シラバスからの検索
def gen_card_syllabus(dic,major):

    """
    dic = {"subject":"思想と...",
             "title":"現代における...",
             "teacher":"佐藤...",
             "code":"01234",
             "semester":"１セメ",
             "day_time":"火１",
             "classes":"医保..." }

    ==Return==
        origin_json :取得したdicのデータでテンプレから変更したjsonデータ

    """
    """
    ['人間論',
    '思想と倫理の世界(World of Thoughts and Ethics)',
    '現代における人間の探究―哲学的人間学入門―_x000D_/Exploration into Human Beings in the Present Age: An Introduction into Philosophical Anthropology',
    '佐藤\u3000透',
    'CB21110',
    '1セメ',
    '火1',
    '医保歯薬工',
    None]
    """


    subject = dic[1].split("(")[0] if "(" in dic[1] else dic[1]
    title = dic[2]
    teacher = dic[3].replace('\u3000', ' ')
    code = dic[4]
    semester = dic[5]
    day_time = dic[6]
    classes = dic[7]#.replace("組","").replace("１～５","機知").replace("６～１０","情物").replace("１１～１２","化バイ").replace("１３～１４","材料").replace("１５～１６","建築").replace("６～１４","情報，化バイ，材料").replace("全","文教法経")

    # colors = ["#bce2e8","#89c3eb","#82ae46","#164a84","#f39800","#ffd900","#e95464"]
    # post_data = ["人間論","人文科学","自然論","自然科学","社会論","社会科学","英語C"]

    colors = {"人間論":"#59b9c6","人文科学":"#2ca9e1","自然論":"#c3d825","自然科学":"#38b48b","社会論":"#ffd900","社会科学":"#f39800","外国語":"#e95464"}
    color = colors[major]

    dcit_card = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": subject,
        "size": "xl",
        "margin": "sm",
        "weight": "bold",
        "style": "italic"
      },
      {
        "type": "text",
        "text": title,
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
                "text": teacher,
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
                "text": semester,
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
                "text": day_time,
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
                "text": classes,
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
          "uri": "https://craft.cite.tohoku.ac.jp/qsl/syllabus/display/" + code
        },
        "color": color
      },
      {
        "type": "button",
        "style": "secondary",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "鬼仏検索",
          "text": subject + "_" + teacher
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

    return dcit_card



def gen_card_onihotoke(dic):

    """
    dic = {'subject': '思想と...',
        'teacher': '佐藤...',
        'difficulty': '仏',
        'worth': 'あり',
        'comment': '非常に有意義でした',
        'test': 'なーい',
        'report': '重すぎます',
        'attendance': '毎回',
        'post date':'2020年04月13日'}

    ==Return==
        origin_json :取得したdicのデータでテンプレから変更したjsonデータ

    """

    subject = dic["subject"] if dic["subject"] else " "
    teacher = dic["teacher"] if dic["teacher"] else " "
    difficulty = dic["difficulty"] if dic["difficulty"] else " "
    worth = dic["worth"] if dic["worth"] else " "
    test = dic["test"] if dic["test"] else " "
    report = dic["report"] if dic["report"] else " "
    attendance = dic["attendance"] if dic["attendance"] else " "
    postdate = dic["post date"] if dic["post date"] else " "
    comment = dic["comment"] if dic["comment"] else " "

    #difficultyに応じてヘッダーの色を変更
    if "仏" in difficulty:
        color_cord = "#fffacd"
    elif "鬼" in difficulty:
        color_cord = "#f08080"
    else:
        color_cord = "#b0c4de"


    dict_card = {
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
    "backgroundColor": color_cord
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": subject,
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
                "text": teacher,
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
                "text": difficulty,
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
                "text": worth,
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
                "text": test,
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
                "text": report,
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
                "text": attendance,
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
                "text": postdate,
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
                "text": comment,
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




    return dict_card
