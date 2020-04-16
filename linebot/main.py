import os
from flask import Flask, request, abort
import requests
import json
import random

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError,LineBotApiError
)
from linebot.models import (
    MessageEvent, FollowEvent,PostbackEvent,TextMessage, TextSendMessage,ButtonsTemplate,TemplateSendMessage,ImageMessage,MessageAction,URIAction,PostbackAction,
    RichMenu,RichMenuSize,RichMenuArea,RichMenuBounds,CarouselTemplate,CarouselColumn,PostbackTemplateAction,BubbleContainer,BoxComponent,TextComponent,ImageComponent,
    FlexSendMessage,FlexSendMessage,CarouselContainer,QuickReply,QuickReplyButton,UnfollowEvent)

from database.syllabus_db import search_lecture_info
from database.user_db import get_userinfo_list, del_userinfo, add_userinfo,get_usermajor,del_userinfo
from database.onihotoke_db import searchTeacher, searchLecture, searchAll
from func import gen_card_syllabus, gen_card_onihotoke

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

major_list = {"文学部":None,
              "教育学部":None,
              "法学部":None,
              "経済学部":None,
              "理学部":None,
              "医学部":None,
              "歯学部":None,
              "薬学部":None,
              "工学部":["機知","情物","化バイ","材料","建築"],
              "農学部":None}

################################################################################################
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

#####################################################################################
@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="""追加ありがとうございます。
東北大学鬼仏LINEbotです。
公開から半年、さらにパワーアップしてリニューアルです！
従来の機能に加えて基幹科目をシラバスから検索できる機能を追加しました！
所属学部を登録することで、自分が履修できる講義が一目瞭然！\n
～使い方～
「講義名」、または「教官の名前」を送信してください。
みなさんの鬼仏情報を見ることができます。\n
さらに下のメニューバー「基幹科目等の検索はこちら」から、自分の所属学部で履修できる基幹科目の講義を検索できます。\n
その他わからないことがありましたら下のメニューバーの「ヘルプ」ボタンを押してください。"""),
            TextSendMessage(
            text="下のボタンから学部を選択してください。\n学部を間違えて登録した際は、「学部再登録」と送信してください。もう一度ボタンが出現します。",
            quick_reply=QuickReply(
                items=[QuickReplyButton(action=PostbackAction(label=major, data=major)) for major in major_list.keys()]
            ))]) # QuickReplyというリッチメッセージが起動してPostbackEventを発生させる

    # slackに投稿
    SLACKBOT_WEBHOOK_URL = os.environ["SLACKBOT_NEW_COMER"]
    profile = line_bot_api.get_profile(event.source.user_id)
    text = "表示名:{}\nユーザID:{}\n画像のURL:{}\nステータスメッセージ:{}".format(profile.display_name, profile.user_id, profile.picture_url, profile.status_message)
    requests.post(SLACKBOT_WEBHOOK_URL, data=json.dumps({'text':text}))

################################################################################################

# ブロックされたときにDBからユーザー情報を削除
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    userid = event.source.user_id
    del_userinfo(userid)

################################################################################################

@handler.add(PostbackEvent)
def on_postback(event):
    user_id = event.source.user_id
    reply_token = event.reply_token
    post_data = event.postback.data

    if post_data=="工学部":
         line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(
            text="下のボタンから学科を選択してください。",
            quick_reply=QuickReply(
                items=[QuickReplyButton(action=PostbackAction(label=major, data=major)) for major in major_list["工学部"]]
            ))])

    elif post_data=="ヘルプ":
        line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text="""再登録をしたいとき・・・
下の「学部再登録」のボタンを押してください。もう一度下にボタンが出現します。\n
さらに詳しい使い方が知りたいとき・・・
「使い方」のボタンを押してください。詳しい使い方を説明します。\n
ご感想、ご要望・・・
「送信フォーム」のボタンを押してください。Googleフォームが現れ、匿名で送信できます。\n
さらに経済学部に特化した「ゼミ協（東北大経済学部）」という情報発信LINEbotもあります。経済学部の方は「ゼミ協」と送信してみてください！"""),
                TemplateSendMessage(
                    alt_text = "選択ボタン",
                    template = ButtonsTemplate(
                    text="以下から選択してください",
                    image_size="cover",
                    actions=[
                            MessageAction(text="学部再登録",
                                        label="学部再登録"),
                            MessageAction(text="使い方",
                                        label="使い方"),
                            MessageAction(text="送信フォーム",
                                        label="送信フォーム"),
                            ]))])

    # 絞り込み検索
    elif post_data[-1]=="論" or post_data[-1]=="学" or post_data[-1]=="語":
        lecture_group = post_data
        print(lecture_group)
        user_major = get_usermajor(user_id)
        print(user_major) #useridを受け取ってDBからそのユーザの所属を返す
        lecture_info = search_lecture_info(lecture_group, user_major) # 講義情報の辞書のリストが返ってくる
        print(lecture_info)
        print(user_major=="工" and post_data=="自然科学")
        if (user_major=="機知" or user_major=="情物" or user_major=="化バイ" or user_major=="材料" or user_major=="建築" or user_major=="理") and post_data=="自然科学":
             line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="件数が多いため表示できません"))

        if len(lecture_info) <=10:
            line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(
                        alt_text='hello',
                        contents=CarouselContainer([gen_card_syllabus(dic,post_data) for dic in lecture_info[:10]])))

        elif 10<len(lecture_info) and len(lecture_info)<=20:
            line_bot_api.reply_message(
                    event.reply_token,
                    [FlexSendMessage(
                        alt_text='hello',
                        contents=CarouselContainer([gen_card_syllabus(dic,post_data) for dic in lecture_info[:10]])),
                    FlexSendMessage(
                        alt_text='hello',
                        contents=CarouselContainer([gen_card_syllabus(dic,post_data) for dic in lecture_info[10:]]))])

        elif 20<len(lecture_info) and len(lecture_info)<=30:
            line_bot_api.reply_message(
                    event.reply_token,
                    [FlexSendMessage(
                        alt_text='hello',
                        contents=CarouselContainer([gen_card_syllabus(dic,post_data) for dic in lecture_info[:10]])),
                    FlexSendMessage(
                        alt_text='hello',
                        contents=CarouselContainer([gen_card_syllabus(dic,post_data) for dic in lecture_info[10:20]])),
                    FlexSendMessage(
                        alt_text='hello',
                        contents=CarouselContainer([gen_card_syllabus(dic,post_data) for dic in lecture_info[20:30]]))])





        # elif len(lecture_info) > 10:
        #     line_bot_api.reply_message(
        #             event.reply_token,
        #             [FlexSendMessage(
        #                 alt_text='hello',
        #                 contents=CarouselContainer([gen_card_syllabus(dic,post_data) for dic in lecture_info[:10]])),
        #             FlexSendMessage(
        #                 alt_text='hello',
        #                 contents=CarouselContainer([gen_card_syllabus(dic,post_data) for dic in lecture_info[10:]]))])
        # else:
        #     line_bot_api.reply_message(
        #             event.reply_token,
        #             FlexSendMessage(
        #                 alt_text='hello',
        #                 contents=CarouselContainer([gen_card_syllabus(dic,post_data) for dic in lecture_info[:10]])))


    else: # ユーザ情報をDBに格納
        if post_data[-1] == "部":
            user_major = post_data[0]
        else:
            user_major = post_data
        add_userinfo(user_major, user_id)
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=post_data + "で登録しました！"))

#####################################################################################
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text

    if text == "学部再登録":
        userid = event.source.user_id
        del_userinfo(userid) # user情報を削除

        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="現在登録されていた学部は削除されました。"),
                TextSendMessage(
                text="もう一度下のボタンから学部を選択してください。",
                quick_reply=QuickReply(
                    items=[QuickReplyButton(action=PostbackAction(label=major, data=major)) for major in major_list]
                ))])

    if text == "使い方":
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text="まんじい"),
            TextSendMessage(text="まんじい")
            ])

    if text == "送信フォーム":
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(
                alt_text = "送信フォーム",
                template = ButtonsTemplate(
                text="送信フォーム",
                image_size="cover",
                actions=[
                        URIAction(
                            uri="https://forms.gle/cAMusm8ZN8i4SmbL8",
                            label="ご感想、ご要望はこちら"
                        )])))

    #教官または講義名いずれかが送信されたとき.もしくはもう一度探すとき
    elif "_" not in text or "でもう一度探す" in text:
        if "でもう一度探す" in text:
            text = text.split("_")[0]
        teacherList = searchTeacher(text, False)#教員列からワードを検索
        lectureList = searchLecture(text, False)#講義列からワードを検索
        kibutsuList = []#2つのリストを結合　1つは空であるはず.
        kibutsuList.extend(teacherList)
        kibutsuList.extend(lectureList)

        #検索結果が空でないとき,その検索結果をlabelにもつボタンを送信.
        if kibutsuList:
            #kibutsuListの要素数が20を超えないようにする.
            if len(kibutsuList)>19:
                kibutsuList = sample(kibutsuList, 19)#一応シャッフルする.何回か表示すればすべての講義を見れるように.
            kibutsuList.extend(["でもう一度探す"])#20個目
            buttons_templates = []
            roop = (len(kibutsuList)+3)//4    #最大4つまで表示できるテンプレートを何回表示すればいいか.

            for i in range(roop):#その回数だけ回す.
                if i==roop-1:#最後は4つ以下になるからスライス部分を変える必要あり.
                    buttons_templates.append(ButtonsTemplate(
                        title='講義名を選択してください', text='choose the lecture name', actions=[
                            MessageAction(label= text + " " + name, text= text + "_" + name) for name in kibutsuList[4*i:]
                            ]))
                    break
                buttons_templates.append(ButtonsTemplate(
                    title='講義名を選択してください', text='choose the lecture name', actions=[
                        MessageAction(label= text + " " + name, text= text + "_" + name) for name in kibutsuList[4*i:4*(i+1)]
                        ]))
            try:
                line_bot_api.reply_message(event.reply_token,
                    [TemplateSendMessage(alt_text='講義を選択してください', template=buttons_template) for buttons_template in buttons_templates])
                # slackに報告
                SLACKBOT_WEBHOOK_URL = os.environ["SLACKBOT_SEARCH_KEYWORD"]
                requests.post(SLACKBOT_WEBHOOK_URL, data=json.dumps({'text':"検索ワード : " + text}))
            except:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="エラーのため講義情報を表示できません.エラーは報告済みです.\nhttps://twitter.com/reiwachan_"))
                # slackに報告
                SLACKBOT_WEBHOOK_URL = os.environ["SLACKBOT_ERROR_KEYWORD"]
                requests.post(SLACKBOT_WEBHOOK_URL, data=json.dumps({'text':"エラー検索ワード : " + text}))

        # 該当する講義がなかったとき
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='該当する講義情報が見つかりませんでした.\nもう一度検索名を見直してください.\
                \n\nバグ,要望等がございましたら\nこちらまでご連絡ください.\nhttps://twitter.com/reiwachan_'))
            # slackに報告
            SLACKBOT_WEBHOOK_URL = os.environ["SLACKBOT_ERROR_KEYWORD"]
            requests.post(SLACKBOT_WEBHOOK_URL, data=json.dumps({'text':"見つからなかった検索ワード : " + text}))


    #教官名と講義名のどちらも送信されたとき、その講義の鬼仏情報をユーザーに送信
    elif "_" in text:
        texts = text.split("_")#『教官名_講義名』　という入力を期待している
        kibutsuList = searchAll(texts[0], texts[1].split("，")[0])#講義情報の辞書のリスト
        print(kibutsuList)
        if kibutsuList :
            if len(kibutsuList)>10:
                kibutsuList = sample(kibutsuList, 10)#一応シャッフルする.何回か表示すればすべての講義を見れるように.

            try:
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(
                        alt_text='鬼仏情報',
                        contents=CarouselContainer([gen_card_onihotoke(dic) for dic in kibutsuList)))
                # slackに報告
                SLACKBOT_WEBHOOK_URL = os.environ["SLACKBOT_SEARCH_KEYWORD"]
                requests.post(SLACKBOT_WEBHOOK_URL, data=json.dumps({'text':"検索ワード : " + text}))
            except:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="エラーのため講義情報を表示できません.エラーは報告済みです.\nhttps://twitter.com/reiwachan_"))
                # slackに報告
                SLACKBOT_WEBHOOK_URL = os.environ["SLACKBOT_ERROR_KEYWORD"]
                requests.post(SLACKBOT_WEBHOOK_URL, data=json.dumps({'text':"エラー検索ワード : " + text}))

        # 該当する講義がなかったとき
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='該当する講義情報が見つかりませんでした.\nもう一度検索名を見直してください.\
                \n\nバグ,要望等がございましたら\nこちらまでご連絡ください.\nhttps://twitter.com/reiwachan_'))
            # slackに報告
            SLACKBOT_WEBHOOK_URL = os.environ["SLACKBOT_ERROR_KEYWORD"]
            requests.post(SLACKBOT_WEBHOOK_URL, data=json.dumps({'text':"見つからなかった検索ワード : " + text}))


    #検索結果が空だったとき、その旨をユーザーに送信
    else :
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='教官名または講義名を入力してください.\
            \n\nバグ,要望等がございましたら\nこちらまでご連絡ください.\nhttps://twitter.com/reiwachan_'))
        # slackに報告
        SLACKBOT_WEBHOOK_URL = os.environ["SLACKBOT_ERROR_KEYWORD"]
        requests.post(SLACKBOT_WEBHOOK_URL, data=json.dumps({'text':"たぶん適当な検索ワード : " + text}))

#####################################################################################

rich_menu_to_create = RichMenu(
    size = RichMenuSize(width=2500, height=1686),
    selected = False,
    name = 'richmenu for randomchat',
    # chat_bar_text = 'id_default',
    chat_bar_text = "基幹科目等の検索はこちら",
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=93, width=675, height=750),
            action=PostbackAction(data="人間論")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=843, width=675, height=750),
            action=PostbackAction(data="人文科学")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=675, y=93, width=575, height=750),
            action=PostbackAction(data="自然論")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=675, y=843, width=575, height=750),
            action=PostbackAction(data="自然科学")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1250, y=93, width=575, height=750),
            action=PostbackAction(data="社会論")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1250, y=843, width=575, height=750),
            action=PostbackAction(data="社会科学")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1825, y=93, width=675, height=750),
            action=PostbackAction(data="外国語")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1825, y=843, width=675, height=750),
            action=PostbackAction(data="ヘルプ")
        )
    ]
)
richMenuId = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

# upload an image for rich menu
# path_default = "job_hisyo_woman_kochira__.png"
# path = "rich_menu.jpg"
with open("static/rich_menu.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image(richMenuId, "image/jpeg", f)

#########################################################################################

# set the default rich menu----------------------------------------------------------------------------
line_bot_api.set_default_rich_menu(richMenuId)
#--------------------------------------------------------------------------------------------------------

#ngrokでデバック用
# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)
