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
    def __init__(self) -> None:
        pass
    
    def quickreply(self, reply_token):
        body = {
            'replyToken': reply_token,
            "messages":[
                {
                    "type": "text",
                    # "text": "select URL or Name",
                    "text": "表示または保存",
                    "quickReply":{
                        "items": [
                            {
                                "type": "action",
                                "action": {
                                    "type": "message",
                                    "label": "表示",
                                    "text": "表示して",
                                }
                            },
                            {
                                "type": "action",
                                "action": {
                                    "type": "postback",
                                    "label": "保存",
                                    "data": "action=save",
                                    "displayText": "保存",
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


class CategorySelect():
    def __init__(self) -> None:
        pass


    def CS_reply(self, reply_token):
        body = {
            'replyToken': reply_token,
            "messages":[
                {
                    "type": "text",
                    "text": "カテゴリーを選択してね",
                    "quickReply":{
                        "items": [
                            {
                                "type": "action",
                                "action": {
                                    "type": "message",
                                    "label": "食事",
                                    "text": "食べに行きたいお店を登録",
                                }
                            },
                            {
                                "type": "action",
                                "action": {
                                    "type": "message",
                                    "label": "旅行",
                                    "text": "行きたい場所を登録",
                                }
                            },
                            {
                                "type": "action",
                                "action": {
                                    "type": "message",
                                    "label": "風俗",
                                    "text": "行きたい風俗を登録",
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



        def CS_reply_show(self, reply_token):
            body = {
                'replyToken': reply_token,
                "messages":[
                    {
                        "type": "text",
                        "text": "カテゴリーを選択してね",
                        "quickReply":{
                            "items": [
                                {
                                    "type": "action",
                                    "action": {
                                        "type": "postback",
                                        "label": "食事",
                                        "data": "show_lunch",
                                        "Desplaytext": "食べに行きたいお店を表示",
                                    }
                                },
                                {
                                    "type": "action",
                                    "action": {
                                        "type": "postback",
                                        "label": "旅行",
                                        "data": "show_travel",
                                        "text": "行きたい場所を表示",
                                    }
                                },
                                {
                                    "type": "action",
                                    "action": {
                                        "type": "postback",
                                        "label": "風俗",
                                        "data": "show_brothel",
                                        "text": "行きたい風俗を表示",
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
