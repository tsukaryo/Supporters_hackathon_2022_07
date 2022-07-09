from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import json
import os
import pprint
# from .flex_message_contents import make_contents, make_flex_contents 
REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/reply"
CHANNEL_SECRET = "4767dec262d22735f5d4f085c7800bcd"
ACCESSTOKEN = 'BSLzDq5+3GTnn2uBODxBRI1mxDvzBsUF+mwwULR0CCF5x4MM5NlDeyOmqJdIA3Q2CR+XHqGRYV1b6FZuRTFK6HYqZkiVKXYOiXT5baAySnLLtGuQ/bPHu6KU9DIMlJJUNUgxfFyZ3BVwm2FPy/WfKwdB04t89/1O/w1cDnyilFU='
HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + ACCESSTOKEN
}

def make_contents(image_file, place_name, url_name):
    contents = {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "", #ここに入れたい画像
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "body": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
            {
                "type": "text",
                "text": "", #ここに場所名 ex.平成女学院
                "size": "xl",
                "weight": "bold",
                "align": "center"
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "button",
                "action": {
                    "type": "uri",
                    "label": "WEBSITE",
                    "uri": "" #ここにURL
                }
            }
            ]
        }
    }
    contents["hero"]["url"] = image_file
    contents["body"]["contents"][0]["text"] = place_name
    contents["footer"]["contents"][0]["action"]["uri"] = url_name
    
    return contents

#最終的なcontents作成
def make_flex_contents(contents_list):
    contents = {
    "type": "carousel",
    "contents": contents_list
    }
    return contents


class FlexMessage(): 
    def __init__(self):
        self.contents = {}
        self.contents_list = []
    
    def make_content_dict(self, image_file, place_name, url_name):
        content_dict = make_contents(image_file, place_name, url_name)
        self.contents_list.append(content_dict)
        return 0
    
    def make_flex_massage_content_dict(self):
        self.contents = make_flex_contents(self.contents_list)
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
        pprint.pprint(body)
        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)