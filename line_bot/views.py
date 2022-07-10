from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .utils import message_creater
from .line_message import LineMessage,CategorySelect
from .models import Place,Status,Category
import pprint
from .utils.flex_messages import FlexMessage

import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re

"""
status
0:終わり（特に関係なし）
1:場所の名前入力待ち
2:場所のURL入力まち
5.場所のカテゴリ
3:「行きたい」待ち(URLスタートの時)
4:場所の入力待ち
6:詳細(detail)の入力まち
7:カテゴリー編集
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
            post_back = data["postback"]
            post_back_data = post_back["data"] #postbackのデータが入ってる
            
            recieved_data = ["食事_表示","旅行_表示","風俗_表示","ALL_表示"]
            #登録のためのカテゴリが選ばれた場合
            if Status.objects.filter(status=5):
                print("EVENT:", data)
                #post_back_dataを引数にカテゴリ表示する関数つくって
                status = Status.objects.get(status=5)
                status.status = 6
                place_data = Place.objects.get(id=status.place_id)
                place_data.category = post_back_data
                place_data.save()
                status.save()
                send_text = "詳細や場所を入力してください"
                line_message_send = LineMessage(message_creater.create_single_text_message(send_text))
                line_message_send.reply(reply_token)
                return HttpResponse("ok")

            #表示のためのカテゴリが選ばれた場合(all以外)
            elif post_back_data in recieved_data[0:2]:
                places = Place.objects.filter(category=post_back_data[0:2])
                # image_file = "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png"
                flex = FlexMessage()
                for place in places:
                    flex.make_content_dict(place.image,place.name,place.url)
                flex.make_flex_massage_content_dict()
                flex.reply(reply_token)
                return HttpResponse("ok")

            #表示のためのカテゴリが選ばれた場合(all)
            elif post_back_data == recieved_data[3]:
                places = Place.objects.all()
                # image_file = "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png"
                flex = FlexMessage()
                for place in places:
                    flex.make_content_dict(place.image,place.name,place.url)
                flex.make_flex_massage_content_dict()
                flex.reply(reply_token)

                return HttpResponse("ok")


        #表示用のカテゴリをpostbackした時

        #event_type == message
        else:
            message = data['message']
            # URLが送られてきた時
            if message['text'][:5] == "https" and Status.objects.filter(status=2).exists()==False:
                #「行きたい」というワード待ちのステータスを立ち上げる
                place_data = Place.objects.create(name="default",url=message['text'],\
                    image="https://s.wordpress.com/mshots/v1/" + message['text'])
                
                Status.objects.create(status=3,place_id=place_data.id)
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
            
            if message['text'] in "やめる":
                statuses = Status.objects.exclude(status=0)
                for status in statuses:
                    status.status=0
                    status.save()
                
            

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

            # URLが送られてきた次のメッセージ
            elif  Status.objects.filter(status=3):
                if "行きたい" in message['text']:
                    #名前入力依頼のテキストを送る
                    db_register_url_start(reply_token,message)
                    return HttpResponse("ok")
                else:
                    status = Status.objects.filter(status=3)
                    delete_place = Place.objects.get(id=status.place_id)
                    delete_place.delete()
                    status.status = 0
                    status.save()
            


            
            #URLが送られて、「行きたい」が送られた後に場所が入力された時
            elif Status.objects.filter(status=4):
                db_register_url_start_place(reply_token,message)
                return HttpResponse("ok")

            elif Status.objects.filter(status=6):
                db_register_url_start_detail(reply_token,message)
                return HttpResponse("ok")

            #「カテゴリー追加して」と送られてきた時
            elif "追加して" in message['text']:
                db_add_category(reply_token,message)
                return HttpResponse("ok")
            
            #追加したいカテゴリーを入力した時
            elif Status.objects.filter(status=7):
                db_add_category(reply_token,mesasge)
                return HttpResponse("ok")
            




        return HttpResponse("ok")


def db_register_start(reply_token):
    Status.objects.create(status=1,place_id=0)
    #send message
    send_text = "名前を入力してください"
    line_message_send = LineMessage(message_creater.create_single_text_message(send_text))
    line_message_send.reply(reply_token)
    return 0


# def place_display(reply_token):
#     places = Place.objects.all()
#     place_name = ""
#     place_url = ""
#     for p in places:
#         place_name += p.name + "\n"
#         place_url += p.name + "\n"
#     line_message_output = LineMessage(message_creater.create_single_text_message(place_name))
#     line_message_output.reply(reply_token)
#     return 0

def db_reset(reply_token):
    place = Place.objects.all() #全削除
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
    place_data.image = "https://s.wordpress.com/mshots/v1/" + recieved_url
    status.save()
    place_data.save()
    select_category = CategorySelect()
    select_category.CS_reply_register(reply_token)
    return 0


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
    status.save()
    place_data = Place.objects.get(id=status.place_id)
    place_data.name = message['text']
    place_data.save()
    select_category = CategorySelect()
    select_category.CS_reply_register(reply_token)
    return 0

def db_register_url_start_detail(reply_token,message):
    status = Status.objects.get(status=6)
    status.status = 0
    status.save()
    place_data = Place.objects.get(id=status.place_id)
    place_data.detail = message['text']
    place_data.save()
    send_text_place = "保存しました"
    line_message_send_name = LineMessage(message_creater.create_single_text_message(send_text_place))
    line_message_send_name.reply(reply_token)

def db_add_dec_category(reply_token,message):
    send_text = "追加したいカテゴリー名を入力してください"
    line_message_send = LineMessage(message_creater.create_single_text_message(send_text))
    Status.objects.create(status=7,place_id=0)
    line_message_send.reply(reply_token)
    return 0
    
def db_add_category(reply_token,mesasge):
    status = Status.objects.get(status=7)
    status.status = 0
    status.save()
    recieved_category = message['text']
    Category.objects.create(category=recieved_category)
    

    

