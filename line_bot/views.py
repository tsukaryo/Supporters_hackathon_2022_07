from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .utils import message_creater
from .line_message import LineMessage
from .models import Place

keep_status=0
id = 0

@csrf_exempt
def index_view(request):

    if request.method == 'POST':
        request = json.loads(request.body.decode('utf-8'))
        print(request)
        data = request['events'][0]
        message = data['message']
        reply_token = data['replyToken']
        line_message = LineMessage(message_creater.create_single_text_message(message['text']))

        if message['text'] == "保存して":
            # Place.objects.create(name='Taro', url='Hello, World!')

            #send message
            send_text = "名前を入力してください"
            line_message_send = LineMessage(message_creater.create_single_text_message(send_text))
            line_message_send.reply(reply_token)
            
            #change keep_status = 1
            keep_status = 1
            return HttpResponse("ok")
            
        elif message['text'] == "表示して":
            line_message = LineMessage(message_creater.create_single_text_message)
            line_message.reply(reply_token)
            places = Place.objects.all()
            place_name = ""
            for p in places:
                place_name += p["name"] + "\n"
            
            line_message_output = LineMessage(message_creater.create_single_text_message(place_name))
            line_message_output.reply(reply_token)
            return HttpResponse("ok")
        
        elif keep_status == 1:
            recieved_name_text = message['text']
            d = Place.objects.create(name=recieved_name_text)
            send_text = "urlを入力してください"
            line_message_send = LineMessage(message_creater.create_single_text_message(send_text))
            line_message_send.reply(reply_token)
            id = d.id

            keep_status = 2
        
        elif keep_status == 2:
            line_message = LineMessage(message_creater.create_single_text_message)
            p = Place.objects.get(id == id)
            p.url = line_message
            p.save()
            send_text_place = "保存しました"
            line_message_send_name = LineMessage(message_creater.create_single_text_message(send_text_place))
            line_message_send_name.reply(reply_token)
            keep_status =0
    
        print(line_message)
        
    return HttpResponse("ok")