from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .utils import message_creater
from .line_message import LineMessage
from .models import Place


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
            line_message = LineMessage(message_creater.create_single_text_message("何を保存しますか"))
            line_message.reply(reply_token)
            return HttpResponse("ok")
        elif message['text'] == "表示して":
            line_message = LineMessage(message_creater.create_single_text_message("何を表示しますか"))
            line_message.reply(reply_token)
            # Place.objects.filter(user_id=1)
            return HttpResponse("ok")
        
        print(line_message)
        
    return HttpResponse("ok")