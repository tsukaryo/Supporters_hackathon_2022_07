from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import json

REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/reply"
CHANNEL_SECRET = "4767dec262d22735f5d4f085c7800bcd"
ACCESSTOKEN = 'BSLzDq5+3GTnn2uBODxBRI1mxDvzBsUF+mwwULR0CCF5x4MM5NlDeyOmqJdIA3Q2CR+XHqGRYV1b6FZuRTFK6HYqZkiVKXYOiXT5baAySnLLtGuQ/bPHu6KU9DIMlJJUNUgxfFyZ3BVwm2FPy/WfKwdB04t89/1O/w1cDnyilFU='
HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + ACCESSTOKEN
}

class LineMessage():
    def __init__(self, messages):
        self.messages = messages

    def reply(self, reply_token):
        body = {
            'replyToken': reply_token,
            'messages': self.messages
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

class QuickReply():
    def __init__(self, messages):
        self.messages = messages
    
    def quickreply(self, reply_token):
        body = {
            'replyToken': reply_token,
            # "messages":{
            #     "type": "text",
            #     "text": "select URL or Name",
            #     "quickReply":{
            #         "items": [
            #             {
            #                 "type": "action",
            #                 "action": {
            #                     "type": "message",
            #                     "label": "URL",
            #                     "text": "register_URL"
            #                 }
            #             },
            #             {
            #                 "type": "action",
            #                 "action": {
            #                     "type": "message",
            #                     "label": "Name",
            #                     "text": "register_name"
            #                 }
            #             }
            #         ]
            #     }
            # }
            "messages":[
                {
                    "type": "text",
                    "text": "select URL or Name",
                    "quickReply":{
                        "items": [
                            {
                                "type": "action",
                                "action": {
                                    "type": "message",
                                    "label": "URL",
                                    "text": "Register URL first"
                                }
                            },
                            {
                                "type": "action",
                                "action": {
                                    "type": "message",
                                    "label": "Name",
                                    "text": "Register name first"
                                }
                            }
                        ]
                    }
                }
            ]
        }
        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)
            

class URLMessage():
    def __init__(self, messages):
        self.messages = messages

    def reply(self, reply_token):
        body = {
            'replyToken': reply_token,
            'messages': [
                    {  
                        "type":"uri",
                        "label":"Web",
                        "linkUri":"https://classmethod.jp/",
                        "area": {
                            "x": 0,
                            "y": 0,
                            "width": 520,
                            "height": 1040
                            }
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


class Postback():
    def __init__(self, messages):
        self.messages = messages
    
    def postback(self, reply_token):
        body = {
            'replyToken': reply_token,
            "messages":[
                {
                    "type": "text",
                    "text": "select URL or Name",
                    "quickReply":{
                        "items": [
                            {
                                "type": "action",
                                "action": {
                                    "type": "message",
                                    "label": "URL",
                                    "text": "Register URL first"
                                }
                            },
                            {
                                "type": "action",
                                "action": {
                                    "type": "message",
                                    "label": "Name",
                                    "text": "Register name first"
                                }
                            }
                        ]
                    }
                }
            ]
        }
        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)