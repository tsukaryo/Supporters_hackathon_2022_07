from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .utils import message_creater
from .utils.flex_messages import FlexMessage
from .utils.uri_message import URIMessage
from .line_message import LineMessage,QuickReply,CategorySelect
from .models import Place,Status
import os
import pprint

import json, datetime
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template.loader import render_to_string

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError, LineBotApiError)
from linebot.models import (MessageEvent, TextMessage, FlexSendMessage, BubbleContainer)


"""
status
0:終わり（特に関係なし）
1:場所の名前入力待ち
2:場所のURL入力まち
5.場所のカテゴリ
3:「行きたい」待ち(URLスタートの時)
4:場所の入力待ち
"""

@csrf_exempt
def index_view(request):
    print("REQUEST:", request)
    if request.method == 'POST':
        request = json.loads(request.body.decode('utf-8'))
        print("request:")
        pprint.pprint(request)
        data = request['events'][0]
        event_type = data['type']
        reply_token = data['replyToken']
        

        #postbackしたとき
        if event_type == "postback":
            print("EVENT:", data)
            # post_back = data["postback"]
            # post_back_data = post_back["data"]
            select_category = CategorySelect()
            select_category.CS_reply(reply_token)
            return HttpResponse("ok")

        #event_type == message
        else:
            message = data['message']
            # URLが送られてきた時
            if message['text'][:5] == "https":
                #「行きたい」というワード待ちのステータスを立ち上げる
                place_data = Place.objects.create(name="default",url=message['text'])
                Status.objects.create(status=3,place_id=place_data.id)
                return HttpResponse("ok")

            # 「web」と送られてきた時
            if message['text'] == "web":
                line_urlreply_send = URIMessage(message_creater.create_single_text_message("test"))
                line_urlreply_send.reply(reply_token)
                return HttpResponse("ok")

            # 「クイック」とメッセージが送られた時
            if message['text'] == "クイック":
                line_quickreply_send = QuickReply()
                line_quickreply_send.quickreply(reply_token)
                return HttpResponse("ok")


            # 「保存して」とメッセージが送られた時
            if message['text'] == "保存して":
                db_register_start(reply_token)
                return HttpResponse("ok")
                
            # 「表示して」とメッセージが送られた時
            elif message['text'] == "表示して":
                select_category = CategorySelect()
                select_category.CS_reply_show(reply_token)
                return HttpResponse("ok")
            

            # 「リセットして」とメッセージが送られた時
            elif message['text'] == "リセットして":
                db_reset(reply_token)
                return HttpResponse("ok")
            
            # 保存したい場所の名前を取得した時
            elif Status.objects.filter(status=1):
                db_register_name(reply_token,message)
                return HttpResponse("ok")
            
            # 保存したい場所のURLを取得した時
            elif Status.objects.filter(status=2):
                db_register_url(reply_token,message)
                return HttpResponse("ok")

            # 保存したい場所のカテゴリーを取得した時
            elif Status.objects.filter(status=5):
                db_register_category(reply_token,message)
                return HttpResponse("ok")

            # URLが送られてきた後に"行きたい"というメッセージが来た時
            elif  Status.objects.filter(status=3):
                if "行きたい" in message['text']:
                    db_register_url_start(reply_token,message)
                    return HttpResponse("ok")
                else:
                    status = Status.objects.filter(status=3)
                    status.status = 0
            
            #URLが送られて、「行きたい」が送られた後に場所が入力された時
            elif Status.objects.filter(status=4):
                db_register_url_start_place(reply_token,message)
                return HttpResponse("ok")
            
                
        return HttpResponse("ok")


def db_register_start(reply_token):
    Status.objects.create(status=1,place_id=0)
    #send message
    send_text = "名前を入力してください"
    line_message_send = LineMessage(message_creater.create_single_text_message(send_text))
    line_message_send.reply(reply_token)
    return 0

def place_display(reply_token):
    places = Place.objects.all()
    place_name = ""
    place_url = ""
    for p in places:
        place_name += p.name + "\n"
        place_url += p.name + "\n"
    line_message_output = LineMessage(message_creater.create_single_text_message(place_name))
    line_message_output.reply(reply_token)
    return 0

def db_reset(reply_token):
    place = Place.objects.all() #全削除
    #place = Place.objects.get(name = "名前1") #一部だけ削除
    place.delete()
    send_text = "リセットしました"
    line_message_send = LineMessage(message_creater.create_single_text_message(send_text))
    line_message_send.reply(reply_token)
    return 0

def db_register_name(reply_token,message):
    status = Status.objects.get(status=1)
    status.status = 2
    recieved_name_text = message['text']
    place_data = Place.objects.create(name=recieved_name_text,url="default")
    print("名前をデータベースに登録しました")
    send_text = "urlを入力してください"
    line_message_send = LineMessage(message_creater.create_single_text_message(send_text))
    line_message_send.reply(reply_token)
    status.place_id = place_data.id
    status.save()
    return 0

def db_register_url(reply_token,message):
    status = Status.objects.get(status=2)
    status.status = 5
    recieved_url = message['text']
    print("keep_status==2に入りました。")
    place_data = Place.objects.get(id=status.place_id)
    print(f"名前と一致するidをデータベースから入手しました。ちなみにidは{place_data.id}です")
    #urlをデータベースに登録
    place_data.url = recieved_url
    status.save()
    place_data.save()
    send_text_place = "カテゴリーを入力してください"
    
    line_message_send_name = QuickReply(message_creater.create_single_text_message(send_text_place))
    line_message_send_name.reply(reply_token)
    return 0

def db_register_category(reply_token,message):
    status = Status.objects.get(status=5)
    print("keep_status==5に入りました。")
    #登録し終えたので0に戻す
    status.status = 0
    received_category = message['text']
    #categoryをデータベースに登録
    place_data = Place.objects.get(id=status.place_id)
    place_data.category = received_category
    status.save()
    place_data.save()
    send_text_place = "保存しました"
    line_message_send_name = LineMessage(message_creater.create_single_text_message(send_text_place))
    line_message_send_name.reply(reply_token)
    return 0

# def db_register_category(reply_token,message):
#     status = Status.objects.get(status=5)
#     print("keep_status==5に入りました。")
#     #登録し終えたので0に戻す
#     status.status = 0
#     #quickreplyでカテゴリーを選択
#     received_category = QuickReply()
#     #categoryをデータベースに登録
#     place_data = Place.objects.get(id=status.place_id)
#     place_data.category = received_category
#     status.save()
#     place_data.save()
#     send_text_place = "保存しました"
#     line_message_send_name = LineMessage(message_creater.create_single_text_message(send_text_place))
#     line_message_send_name.reply(reply_token)
#     return 0


#テスト
# line_quickreply_send = QuickReply()
# line_quickreply_send.quickreply(reply_token)
# return HttpResponse("ok")


#URLスタートでdbへの保存をするとき
def db_register_url_start(reply_token,message):
    status = Status.objects.get(status=3)
    status.status = 4
    status.save()
    send_text_place = "行きたい場所の名前はなんですか"
    line_message_send_name = LineMessage(message_creater.create_single_text_message(send_text_place))
    line_message_send_name.reply(reply_token)
    return 0

# URL始まりで場所が送られてきた時
def db_register_url_start_place(reply_token,message):
    status = Status.objects.get(status=4)
    status.status = 5
    place_data = Place.objects.get(id=status.place_id)
    place_data.name = message['text']
    place_data.save()
    # send_text_place = "カテゴリを入力して"
    # line_message_send_name = LineMessage(message_creater.create_single_text_message(send_text_place))
    select_category = CategorySelect()
    select_category.CS_reply(reply_token)
    # line_message_send_name.reply(reply_token)
    return 0

# Flexmessageで表示
# line_bot_api = LineBotApi(channel_access_token=settings.ACCESSTOKEN)
# handler = WebhookHandler(channel_secret=settings.CHANNEL_SECRET)
# @handler.add(MessageEvent, message=TextMessage)
def handle_message(reply_token,message):
    msg_text = "あなたの行きたい場所"
    places = Place.objects.all()
    place_name = ""
    place_url = ""
    for p in places:
        place_name += p.name + "\n"
        place_url += p.url + "\n"
    # output_placename = LineMessage(message_creater.create_single_text_message(place_name))
    line_message_send_name = FlexMessage(message_creater.create_single_text_message("test"))
    line_message_send_name.reply(reply_token)
    # msg = render_to_string("./message.json", {"text": msg_text, "place":output_placename })
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     FlexSendMessage(alt_text = msg_text, contents = json.loads(msg))
    # )