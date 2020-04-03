#LINEのユーザーインターフェース部分
import os
import errno
import tempfile
from random import sample
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)

from search_sql import searchLecture, searchTeacher, searchAll
from gspred import setsheet, search_last_row, record_keyword, record_error, record_notExist, record_userinfo


setsheet()
app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN') #アクセストークンを入れてください
handler = WebhookHandler('YOUR_CHANNEL_SECRET') #Channel Secretを入れてください


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

    #テキストメッセージが送信されたときの処理.
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text

    #教官または講義名いずれかが送信されたとき.
    if "_" not in text:
        teacherList = searchTeacher(text, False)#教員列からワードを検索
        lectureList = searchLecture(text, False)#講義列からワードを検索

        kibutsuList = []#2つのリストを結合　1つは空であるはず.
        kibutsuList.extend(teacherList)
        kibutsuList.extend(lectureList)

        #検索結果が空でないとき,その検索結果をlabelにもつボタンを送信.
        if kibutsuList:
            #kibutsuListの要素数が20を超えないようにする.
            if len(kibutsuList)>18:
                kibutsuList = sample(kibutsuList, 18)#一応シャッフルする.何回か表示すればすべての講義を見れるように.


            kibutsuList.extend(["のすべての講義"])#19個目.
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
               #record_keyword(text)

            except LineBotApiError:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="エラーのため講義情報を表示できません.エラーは報告済みです.\nhttps://twitter.com/reiwachan_"))
                #record_error(text)

        #検索結果が空だったとき、その旨をユーザーに送信
        else :
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='該当する講義情報が見つかりませんでした.\nもう一度検索名を見直してください.\
                \n\nバグ,要望等がございましたら\nこちらまでご連絡ください.\n講義数が多い場合はその一部を表示しています.\nhttps://twitter.com/reiwachan_'))
            #record_notExist(text)

    #もう一度探すとき
    elif "でもう一度探す" in text:
        text = text.split("_")[0]

        teacherList = searchTeacher(text, False)#教員列からワードを検索
        lectureList = searchLecture(text, False)#講義列からワードを検索

        kibutsuList = []#2つのリストを結合　1つは空であるはず.
        kibutsuList.extend(teacherList)
        kibutsuList.extend(lectureList)

        #検索結果が空でないとき,その検索結果をlabelにもつボタンを送信.
        if kibutsuList:
            #kibutsuListの要素数が20を超えないようにする.
            if len(kibutsuList)>18:
                kibutsuList = sample(kibutsuList, 18)#一応シャッフルする.何回か表示すればすべての講義を見れるように.

            kibutsuList.extend(["でもう一度探す"])#19個目
            kibutsuList.extend(["のすべての講義"])#これで丁度20こ目.

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
                #record_keyword(text)

            except LineBotApiError:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="エラーのため講義情報を表示できません.エラーは報告済みです.\nhttps://twitter.com/reiwachan_"))
                #record_error(text)

        #検索結果が空だったとき、その旨をユーザーに送信
        else :
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='該当する講義情報が見つかりませんでした.\nもう一度検索名を見直してください.\
                \n\nバグ,要望等がございましたら\nこちらまでご連絡ください.\n講義数が多い場合はその一部を表示しています.\nhttps://twitter.com/reiwachan_'))
            #record_notExist(text)

    #『〇〇のすべての講義』のボタンが押されたとき、その〇〇の検索結果をすべて表示
    elif "のすべての講義" in text:
        text = text.split("_")[0]#リストになってる

        teacherList = searchTeacher(text, True)#教員列からワードを検索
        lectureList = searchLecture(text, True)#講義列からワードを検索

        kibutsuList = []#2つのリストを結合　1つは空であるはず
        kibutsuList.extend(teacherList)
        kibutsuList.extend(lectureList)

        messages =[]
        print(len(kibutsuList))
        if kibutsuList:
        #フォーマットを整える
            if len(kibutsuList)<5:#4件しかないときはほぼ確実に送れる
                for kibutsuDict in kibutsuList:#5件まで.
                    message = ""
                    for key, value in kibutsuDict.items():
                        message += key + " : " + value + "\n"
                        message += "--------------------------\n"
                    messages.append(message)
            else:#4件以上あるときは文字数オーバーする可能性があるため,同じ吹き出しに複数個の講義情報をのせる
                message = ""
                for kibutsuDict in kibutsuList:
                    for key, value in kibutsuDict.items():
                        message += key + " : " + value + "\n"
                        message += "--------------------------\n"
                    message += "\n####################\n\n"
                    if len(message)>1250:#一度に送れるのが2000文字までなので,一応1250文字を超えていたら別にわける.
                        messages.append(message)
                        message = ""

            #最後にツイッターのリンクをつける
            messages.append("バグ,要望等がありましたらこちらまでご連絡ください.\n講義数が多い場合はその一部を表示しています.\nhttps://twitter.com/reiwachan_")
            try:
                line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=message) for message in messages[-4:]])#5つだけ送信（すべてではない）
                #record_keyword(text)

            except LineBotApiError:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="エラーのため講義情報を表示できません.エラーは報告済みです.\nhttps://twitter.com/reiwachan_"))
                #record_error(text)

        #検索結果が空だったとき、その旨をユーザーに送信
        else:
            line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='該当する講義情報が見つかりませんでした.\nもう一度検索名を見直してください.\
                \n\nバグ,要望等がございましたら\nこちらまでご連絡ください.\n講義数が多い場合はその一部を表示しています.\nhttps://twitter.com/reiwachan_'))
            #record_notExist(text)

    #教官名と講義名のどちらも送信されたとき、その講義の鬼仏情報をユーザーに送信
    elif "_" in text:
        texts = text.split("_")#『教官名_講義名』　という入力を期待している
        kibutsuList = searchAll(texts[0], texts[1])#特定の講義の鬼仏情報を取得

        messages = []
        if kibutsuList:
            #フォーマットを整える
            if len(kibutsuList)<5:#4件しかないときはほぼ確実に送れる
                for kibutsuDict in kibutsuList:#5件まで.
                    message = ""
                    for key, value in kibutsuDict.items():
                        message += key + " : " + value + "\n"
                        message += "--------------------------\n"
                    messages.append(message)
            else:#4件以上あるときは文字数オーバーする可能性があるため,同じ吹き出しに複数個の講義情報をのせる
                message = ""
                for kibutsuDict in kibutsuList:
                    for key, value in kibutsuDict.items():
                        message += key + " : " + value + "\n"
                        message += "--------------------------\n"
                    message += "\n####################\n\n"
                    if len(message)>1250:#一度に送れるのが2000文字までなので,一応1000文字を超えていたら別にわける.
                        messages.append(message)
                        message = ""

            #最後にツイッターのリンクをつける
            messages.append("バグ,要望等がありましたらこちらまでご報告ください.\n講義数が多い場合はその一部を表示しています.\nhttps://twitter.com/reiwachan_")

            #try:
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=message) for message in messages[-5:]])
            #record_keyword(text)

            #except LineBotApiError:
                #line_bot_api.reply_message(event.reply_token,TextSendMessage(text="エラーのため講義情報を表示できません.エラーは報告済みです.\nhttps://twitter.com/reiwachan_"))
                #record_error(text)

        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='該当する講義情報が見つかりませんでした.\nもう一度検索名を見直してください.\
                \n\nバグ,要望等がございましたら\nこちらまでご連絡ください.\n講義数が多い場合はその一部を表示しています.\nhttps://twitter.com/reiwachan_'))
            #record_notExist(text)

    else :
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="教官名または講義名を入力してください.\
            \nバグ,要望等がありましたらこちらまでご報告ください.\nhttps://twitter.com/reiwachan_"))


#友だち追加したときに、そのユーザーの情報がbotから通知される
@handler.add(FollowEvent)
def handle_follow(event):
    #誰が追加したかわかるように機能追加
    profile = line_bot_api.get_profile(event.source.user_id)
    line_bot_api.push_message("U90270fbcc310d31bb0c7bdbaa1e4b01c",
        TextSendMessage(text="表示名:{}\nユーザID:{}\n画像のURL:{}\nステータスメッセージ:{}"\
        .format(profile.display_name, profile.user_id, profile.picture_url, profile.status_message)))

    
    #友達追加したユーザにメッセージを送信
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='◇こんにちは、全脳のれいわちゃんです！◇\n\n「講義名」、または「教官の名前」を送信してください。\nみなさんの鬼仏情報を見ることができます！\n\n◇制作◇\n鬼仏表プロジェクトチーム全脳アーキテクチャ（WBA）若手の会・東北支部\n==Project Chief　\n美濃 佑輝 #B8-Edu\n\n==Chief Engineer　\n高橋 佑輔 #B8-Eng-EIPE\n\n==Database Engineer　\n三好 壮哉 #M1-ICE(東工大)\n深水 一聖 #B8-Eng-MAE \n\n==Infrastructure Engineer　\n伊藤 冬馬 #B7-Sci-Bio\n\n◇連絡先・不具合の報告◇\nhttps://twitter.com/reiwachan_\n\n◇トンペー鬼仏表◇\nhttps://www.tonpe.site/toppages/index'))

    record_userinfo(profile.display_name, profile.user_id, profile.status_message, profile.picture_url)


if __name__ == "__main__":
    app.debug=True
    port = int(os.environ.get('PORT', 8000))
    app.run(host ='0.0.0.0',port = port)
    #app.run(debug=True, port=8000)