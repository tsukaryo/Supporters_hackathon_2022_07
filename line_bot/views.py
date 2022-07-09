from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .utils import message_creater
from .line_message import LineMessage,QuickReply
from .models import Place,Status
import os
import pprint

"""
status
0:終わり（特に関係なし）
1:場所の名前入力待ち
2:場所のURL入力まち
3:場所の名前待ち(URLスタートの時)
"""

@csrf_exempt
def index_view(request):
    if request.method == 'POST':
        request = json.loads(request.body.decode('utf-8'))
        print("request:")
        pprint.pprint(request)
        data = request['events'][0]
        message = data['message']
        reply_token = data['replyToken']
    
        # URLが送られてきた時
        if message['text'][:5] == "https":
            #「行きたい」というワード待ちのステータスを立ち上げる
            place_data = Place.objects.create(name="default",url=message['text'])
            Status.object.create(status=3,place_id=place_data.id)
            return HttpResponse("ok")

        # 「保存して」とメッセージが送られた時
        if message['text'] == "クイック":
            line_quickreply_send = QuickReply(message_creater.create_single_text_message("test"))
            line_quickreply_send.reply(reply_token)
            return HttpResponse("ok")

        # 「保存して」とメッセージが送られた時
        if message['text'] == "保存して":
            db_register_start(reply_token)
            return HttpResponse("ok")
            
        # 「表示して」とメッセージが送られた時
        elif message['text'] == "表示して":
            place_display(reply_token)
            return HttpResponse("ok")
        
        # 保存したい場所の名前を取得した時
        elif Status.objects.filter(status=1):
            db_register_name(reply_token,message)
            return HttpResponse("ok")
        
        # 保存したい場所のURLを取得した時
        elif Status.objects.filter(status=2):
            db_register_url(reply_token,message)
            return HttpResponse("ok")

        # URLが送られてきた後に"行きたい"というメッセージが来た時
        elif  Status.objects.filter(status=3):
            if "行きたい" in message['text']:
                db_register_name(reply_token,message)
                return HttpResponse("ok")
            else:
                status = Status.objects.filter(status=3)
                status.status = 0
            
            
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
    for p in places:
        place_name += p.name + "\n"
    line_message_output = LineMessage(message_creater.create_single_text_message(place_name))
    line_message_output.reply(reply_token)
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
    #登録し終えたので0に戻す
    status.status = 0
    recieved_url = message['text']
    print("keep_status==2に入りました。")
    place_data = Place.objects.get(id=status.place_id)
    print(f"名前と一致するidをデータベースから入手しました。ちなみにidは{p.id}です")
    place_data.url = recieved_url
    status.save()
    place_data.save()
    print("urlをデータベースに登録しました")
    send_text_place = "保存しました"
    line_message_send_name = LineMessage(message_creater.create_single_text_message(send_text_place))
    line_message_send_name.reply(reply_token)
    return 0

    


#URLスタートでdbへの保存をするとき
def db_register_url_start(reply_token,message):
    status = Status.objects.get(status=3)
    status.status = 4
    send_text_place = "行きたい場所の名前はなんですか"
    line_message_send_name = LineMessage(message_creater.create_single_text_message(send_text_place))
    line_message_send_name.reply(reply_token)
    return 0


## Flexmessageで返す
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     msg_text = "あなたの行きたい場所"
#     places = Place.objects.all()
#     place_name = ""
#     for p in places:
#         place_name += p.name + "\n"
#     output_placename = LineMessage(message_creater.create_single_text_message(place_name))
#     msg = render_to_string("message.json", {"text": msg_text, "place":output_placename })
#     line_bot_api.reply_message(
#         event.reply_token,
#         FlexSendMessage(alt_text = msg_text, contents = json.loads(msg))
#     )