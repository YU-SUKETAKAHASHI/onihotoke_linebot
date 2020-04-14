import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,LineBotApiError
)
from linebot.models import (
    MessageEvent, FollowEvent,PostbackEvent,TextMessage, TextSendMessage,ButtonsTemplate,TemplateSendMessage,ImageMessage,MessageAction,URIAction,PostbackAction,
    RichMenu,RichMenuSize,RichMenuArea,RichMenuBounds,CarouselTemplate,CarouselColumn,PostbackTemplateAction,BubbleContainer,BoxComponent,TextComponent,ImageComponent,
    FlexSendMessage,FlexSendMessage,CarouselContainer)

from database.syllabus import get_connection, get_lecture_list, search_lecture_info
from func import gen_card_syllabus
from user_db import get_usermajor, del_userinfo, add_userinfo

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


major_list = ["文学部", "教育学部", "法学部", "経済学部", "理学部", "医学部", "歯学部", "薬学部", "工学部", "農学部"]

################################################################################################
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'


################################################################################################
@handler.add(PostbackEvent)
def on_postback(event):
    user_id = event.source.user_id
    reply_token = event.reply_token
    post_data = event.postback.data

    # 絞り込み検索
    if post_data[-1]=="論" or post_data[-1]=="学" or post_data[-1]=="語":
        lecture_group = post_data
        user_major = get_usermajor(userid) #useridを受け取ってDBからそのユーザの所属を返す
        lecture_info = search_lecture_info(lecture_group, user_major) # 講義情報の辞書のリストが返ってくる

        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text='hello',
                    contents=CarouselContainer([gen_card_syllabus(dic) for dic in lecture_info])))

    else: # ユーザ情報をDBに格納
        user_major = post_data
        add_userinfo(user_major, user_id)

#####################################################################################
@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="友だち追加ありがとうございます。\n\n"),
            TextSendMessage(
            text="下のボタンから学部を選択してください。\n\n学部を間違えて登録した際は、画面下部のメニューバーより再登録することができます。",
            quick_reply=QuickReply(
                items=[QuickReplyButton(action=PostbackAction(label=major, data=major)) for major in major_list]
            ))]) # QuickReplyというリッチメッセージが起動してPostbackEventを発生させる

#####################################################################################
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text

    if text == "学部再登録":
        userid = event.source.user_id
        del_userinfo(userid) # user情報を削除

        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="現在登録されていた学部、研究科は削除されました。"),
                TextSendMessage(
                text="もう一度下のボタンから学部を選択してください。",
                quick_reply=QuickReply(
                    items=[QuickReplyButton(action=PostbackAction(label=major, data=major)) for major in major_list]
                ))])


#####################################################################################

rich_menu_to_create = RichMenu(
    size = RichMenuSize(width=2500, height=1686),
    selected = False,
    name = 'richmenu for randomchat',
    # chat_bar_text = 'id_default',
    chat_bar_text = "選択してください",
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=625, height=843),
            action=PostbackAction(data="人間論")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=843, width=625, height=843),
            action=PostbackAction(data="人文科学")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=625, y=0, width=625, height=843),
            action=PostbackAction(data="自然論")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=625, y=843, width=625, height=843),
            action=PostbackAction(data="自然科学")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1250, y=0, width=625, height=843),
            action=PostbackAction(data="社会論")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1250, y=843, width=625, height=843),
            action=PostbackAction(data="社会科学")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1875, y=0, width=625, height=843),
            action=PostbackAction(data="英語")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1875, y=843, width=625, height=843),
            action=PostbackAction(data="ヘルプ")
        )
    ]
)
richMenuId = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

# upload an image for rich menu
# path_default = "job_hisyo_woman_kochira__.png"
path = "onihotoke.jpg"
with open(path, 'rb') as f:
    line_bot_api.set_rich_menu_image(richMenuId, "image/png", f)

#########################################################################################

# set the default rich menu----------------------------------------------------------------------------
line_bot_api.set_default_rich_menu(richMenuId)
#--------------------------------------------------------------------------------------------------------

#ngrokでデバック用
if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 8080))
#     app.run(host ='0.0.0.0',port = port, debug=True)
