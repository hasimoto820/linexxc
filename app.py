from __future__ import unicode_literals

import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
#import gurunavi



#*******************   gurunavi             ***************
import json
import urllib.request
import ssl
#認証方法をTLSv1に指定
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

# API に渡すパラメータの値の指定
# https://api.gnavi.co.jp/api/manual/restsearch/
# https://api.gnavi.co.jp/api/tools/     #ここでAPIのテストができる
base_url = "https://api.gnavi.co.jp/RestSearchAPI/v3/"

key = '90dc4b25c570c60b83ebefe5d98aedcc'

##### 上記の key は、ぐるなびAPI のアカウントを作成した際、取得したkeyidを指定
# shop_name = "焼肉"　#店名も含める場合はコメントアウト外す
g_code = 'RSFST03001' # 寿司のコード
address = '那覇'

#*******************   gurunavi             ***************










app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = "2929bf7d9211ed8a9d23ee23899c3e54"
channel_access_token = "XrY3Ox3iI311N/JAoU+lqpWrGk98F6qcbmWfraJpaoknQQGWyxbpIFXeYJyf6JM4m2KILBGPb4L6Vn7pjPLzcQstVBWI0QOrUjwFp7WecWXXDt+jh6XDntapWgmV74MkqniQABT8lxICQehzm0dhPQdB04t89/1O/w1cDnyilFU="
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        # 対話形式にする
        if event.message.text == 'Hello' :
            event.message.text = 'world'
        elif event.message.text == '鬼滅' :
            event.message.text = 'の刃'
        elif event.message.txt == 'そば' or event.message.txt == 'soba' or event.message.txt == 'Soba' :


            event.message.text = 'mada tochu'

            params = urllib.parse.urlencode({
                'keyid': key,
                # 'name' : shop_name,　#店名も含める場合はコメントアウト外す
                'category_s' : g_code,
                'address' : address
            })
            url = base_url + '?' + params
            #print(url)
            response = urllib.request.urlopen(url,context=context)
            data = response.read()

            # 取得した情報をJSON形式から辞書型に変換
            read_data = json.loads(data)["rest"]


            # お店の名前の一覧を格納する list の作成
            list_name = []



            # お店の名前の list を取得
            for dic in read_data:
                list_name.append(dic.get("name"))
            ret = list_name

            #event.message.text = str(ret)
            #event.message.text = 'そばを探します'


        else :
            event.message.text = event.message.text + 'ですね'

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

    return 'OK'


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
