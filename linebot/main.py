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

from database.operate import get_connection, get_lecture_list, search_lecture_info

app = Flask(__name__)

LINE_BOT_API = os.environ.get('LINE_BOT_API')
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')

line_bot_api = LineBotApi(LINE_BOT_API) #アクセストークンを入れてください
handler = WebhookHandler(CHANNEL_SECRET) #Channel Secretを入れてください

################################################################################################


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

#--------------------------------------------------------------------------------------------------------------------------

@handler.add(PostbackEvent)
def on_postback(event):
    user_id = event.source.user_id
    reply_token = event.reply_token
    postback_msg = event.postback.data

    if postback_msg == "人間論":

        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(
                    alt_text='hello',
                    contents=CarouselContainer([{

}])))

    elif postback_msg == "自然論":

        line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text="あなたが今セメスターにとれる" + postback_msg + "の講義は以下の通りです"),
                FlexSendMessage(
                    alt_text='hello',
                    contents=CarouselContainer([origin_json,origin_json,origin_json,origin_json

                    ])
                    )
                ]
            )

    elif postback_msg == "社会論":

        line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text="あなたが今セメスターにとれる" + postback_msg + "の講義は以下の通りです"),
                FlexSendMessage(
                    alt_text='hello',
                    contents=CarouselContainer([origin_json

                    ])
                    )
                ]
            )


    elif postback_msg == "英語":

        line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage(text="あなたが今セメスターにとれる" + postback_msg + "の講義は以下の通りです"),
                FlexSendMessage(
                    alt_text='hello',
                    contents=CarouselContainer([origin_json

                    ])
                    )
                ]
            )

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
            bounds=RichMenuBounds(x=1250, y=0, width=625, height=843),
            action=PostbackAction(data="人文科学")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=843, width=625, height=843),
            action=PostbackAction(data="自然論")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1250, y=843, width=625, height=843),
            action=PostbackAction(data="自然科学")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1250, y=843, width=625, height=843),
            action=PostbackAction(data="社会論")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1250, y=843, width=625, height=843),
            action=PostbackAction(data="社会科学")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1250, y=843, width=625, height=1686),
            action=PostbackAction(data="英語")
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
