from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .utils import message_creater
from .line_message import LineMessage
from .models import Place,Status
import os

# keep_status = 0
id = 0

current_dir = os.path.dirname(__file__)
status_file_name = "keep_status.txt"
status_file_path = os.path.join(current_dir, "status", status_file_name)
with open(status_file_path) as f:
    keep_status = int(f.read())

@csrf_exempt
def index_view(request):
    global keep_status,id
    print("KEEP_STATUS IS", keep_status, "NOW.")
    if request.method == 'POST':
        request = json.loads(request.body.decode('utf-8'))
        print("request:")
        print(request)
        data = request['events'][0]
        message = data['message']
        reply_token = data['replyToken']
        line_message = LineMessage(message_creater.create_single_text_message(message['text']))

        # DBに保存するとき
        if message['text'] == "保存して":
            print("MESSAGE[TEXT] == 保存して")
            Status.objects.create(status=1,place_id=0)
            # Place.objects.create(name='Taro', url='Hello, World!')
            #send message
            send_text = "名前を入力してください"
            line_message_send = LineMessage(message_creater.create_single_text_message(send_text))
            line_message_send.reply(reply_token)
            
            #change keep_status = 1
            # keep_status = 1
            with open(status_file_path, mode='w') as f:
                f.write("1")
            print("KEEP_STATUS(GLOBAL):", keep_status)
            return HttpResponse("ok")
            
        # DBの情報を表示するとき
        elif message['text'] == "表示して":
            print("MESSAGE[TEXT] == 表示して")
            places = Place.objects.all()
            print("PLACES = ",places)
            place_name = ""
            print("place[0]: " + str(places[0]))
            for p in places:
                place_name += p["name"] + "\n"
            line_message_output = LineMessage(message_creater.create_single_text_message(place_name))
            line_message_output.reply(reply_token)
            return HttpResponse("ok")
        
        # elif keep_status == 1:
        elif Status.objects.filter(status=1):
            s = Status.objects.get(status=1)
            s.status = 2
            
            print("keep_status==1に入りました")
            recieved_name_text = message['text']
            d = Place.objects.create(name=recieved_name_text,url="default")
            print("名前をデータベースに登録しました")
            send_text = "urlを入力してください"
            line_message_send = LineMessage(message_creater.create_single_text_message(send_text))
            line_message_send.reply(reply_token)
            s.place_id = d.id
            s.save()
            print("before id : "+ str(id))
            # with open(status_file_path, mode='w') as f:
            #     f.write("2")
            # keep_status = 2
            return HttpResponse("ok")
        
        # elif keep_status == 2:
        elif Status.objects.filter(status=2):
            s = Status.objects.get(status=2)
            s.status = 0
            s.save()
            recieved_url = message['text']
            print("keep_status==2に入りました。")
            print("after id : "+ str(id))
            p = Place.objects.get(id=id)
            print(f"名前と一致するidをデータベースから入手しました。ちなみにidは{p}です")
            p.url = recieved_url
            p.save()
            print("urlをデータベースに登録しました")
            send_text_place = "保存しました"
            line_message_send_name = LineMessage(message_creater.create_single_text_message(send_text_place))
            line_message_send_name.reply(reply_token)

            # with open(status_file_path, mode='w') as f:
            #     f.write("0")
            # keep_status =0
            print("keep_status==0にリセット")
            return HttpResponse("ok")
    
        print(line_message)
        
    return HttpResponse("ok")