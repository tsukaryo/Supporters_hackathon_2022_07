from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import json
import os
from .flex_message_contents import make_contents, make_flex_message_contents 
REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/reply"
CHANNEL_SECRET = "4767dec262d22735f5d4f085c7800bcd"
ACCESSTOKEN = 'BSLzDq5+3GTnn2uBODxBRI1mxDvzBsUF+mwwULR0CCF5x4MM5NlDeyOmqJdIA3Q2CR+XHqGRYV1b6FZuRTFK6HYqZkiVKXYOiXT5baAySnLLtGuQ/bPHu6KU9DIMlJJUNUgxfFyZ3BVwm2FPy/WfKwdB04t89/1O/w1cDnyilFU='
HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + ACCESSTOKEN
}

current_dir = os.path.dirname(__file__) #このfileのあるディレクトリパスを取得
file_path = os.path.join(current_dir, "flexmessage.json")
json_open = open(file_path, 'r')
json_load = json.load(json_open)
json_open.close()


class FlexMessage(): 
    def __init__(self):
        self.contents = {}
    
    def make_content_dict(self, image_file, place_name, url_name):
        content_dict = make_contents(image_file, place_name, url_name)
        return content_dict
    
    def make_flex_massage_content_dict(self, contents_list):
        contents_dict = make_flex_message_contents(contents_list)
        self.contents = contents_dict
        return 0

    def reply(self, reply_token):
        body = {
            'replyToken': reply_token,
            "messages": [
                {
                    "type": "flex",
                    "altText": "This is a Flex Message",
                    "contents": self.contents
                }
            ]
        }
        print(body)
        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)