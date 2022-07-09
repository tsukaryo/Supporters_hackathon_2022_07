from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import json
import pprint

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
                                "imageUrl": "https://lh3.googleusercontent.com/pw/AM-JKLXKQPaqZgGsyu-mJYa6urbaYgqzaDV4oM2NtRHy3Sa1ULcY3Sr6hwQU4pPx1PCenkUVs7N6IEY28kCYAKD4Fm6y_UPspmKlTkuAdg0J4x50g6pztO9Qg2HVoET3tkNJebpJswwHDTk9WYwdp3QLBkPSVg=s256-no?authuser=0",
                                "action": {
                                    "type": "message",
                                    "label": "表示",
                                    "text": "表示して",
                                }
                            },
                            {
                                "type": "action",
                                "imageUrl": "https://lh3.googleusercontent.com/pw/AM-JKLWoTbaFMMnFRxWAcFZ0_F7gM24TkiqkZPZKwidzQ4l_iLTzQfah6euxOcsdYNwQTJoJfGyDbch8I7Xb0isxQuufbqJMQ9Nhldt8tK8d0AvILMFNY85HcuCzpTH7rgMLv7GiZK07S_vwWXcKqhtJZ0cIQA=s256-no?authuser=0",
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


    def CS_reply_register(self, reply_token):
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
                                "imageUrl": "https://lh3.googleusercontent.com/pw/AM-JKLUpo7nGeeYZn83C2pxHEP3Mu76CKwJ84JvCrEgjKzBVfInjko_cA9I1f5qAsN23AlIXTrOqY6ymL660GY_QXNS-frllXepApgnTTW3jklnxMiU4k0_J2bX16SOYgfMlHTR_FAmNX1JJBbAfwYDC0CK50A=s256-no?authuser=0",
                                "action": {
                                    "type": "postback",
                                    "label": "食事",
                                    "data": "食事",
                                    "displayText": "食事",
                                }
                            },
                            {
                                "type": "action",
                                "imageUrl": "https://lh3.googleusercontent.com/pw/AM-JKLW9eV0umcXblTMmLEx4PUoRKQ0JEMwLhqroEXxJg5QziilhPI_S0Xjrlr7yL6NgW2i1tOOLXsPEC4PcEdSa6ue1JVTR39tPZQnVdfVTBMqmN9jLzPFc3-fgi8i6OwKpGQegsInLMs86l8X7UjKLHBePiQ=s256-no?authuser=0",
                                "action": {
                                    "type": "postback",
                                    "label": "旅行",
                                    "data": "旅行",
                                    "displayText": "場所",
                                }
                            },
                            {
                                "type": "action",
                                "imageUrl": "https://lh3.googleusercontent.com/pw/AM-JKLW6lsFpdAm3D2p-Lgscv6lU9VGSsMRnpE53JcMv6hmEXLzTC06lS9U1jPaKJejZVgvALHVvU5eENmCoriuGr892VcD6ZAF07d541Kc5eO3ztYij5daq0maBQYAv0v34Z_LXq41MXQ4r1AMmtF_KWxwThA=s256-no?authuser=0",
                                "action": {
                                    "type": "postback",
                                    "label": "風俗",
                                    "data": "風俗",
                                    "displayText": "風俗",
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
                pprint.pprint(body)
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
                                "imageUrl": "https://lh3.googleusercontent.com/pw/AM-JKLUpo7nGeeYZn83C2pxHEP3Mu76CKwJ84JvCrEgjKzBVfInjko_cA9I1f5qAsN23AlIXTrOqY6ymL660GY_QXNS-frllXepApgnTTW3jklnxMiU4k0_J2bX16SOYgfMlHTR_FAmNX1JJBbAfwYDC0CK50A=s256-no?authuser=0",
                                "action": {
                                    "type": "postback",
                                    "label": "食事",
                                    "data": "食事_表示",
                                    "displayText": "食べに行きたいお店を表示",
                                }
                            },
                            {
                                "type": "action",
                                "imageUrl": "https://lh3.googleusercontent.com/pw/AM-JKLW9eV0umcXblTMmLEx4PUoRKQ0JEMwLhqroEXxJg5QziilhPI_S0Xjrlr7yL6NgW2i1tOOLXsPEC4PcEdSa6ue1JVTR39tPZQnVdfVTBMqmN9jLzPFc3-fgi8i6OwKpGQegsInLMs86l8X7UjKLHBePiQ=s256-no?authuser=0",
                                "action": {
                                    "type": "postback",
                                    "label": "旅行",
                                    "data": "旅行_表示",
                                    "displayText": "行きたい場所を表示",
                                }
                            },
                            {
                                "type": "action",
                                "imageUrl": "https://lh3.googleusercontent.com/pw/AM-JKLW6lsFpdAm3D2p-Lgscv6lU9VGSsMRnpE53JcMv6hmEXLzTC06lS9U1jPaKJejZVgvALHVvU5eENmCoriuGr892VcD6ZAF07d541Kc5eO3ztYij5daq0maBQYAv0v34Z_LXq41MXQ4r1AMmtF_KWxwThA=s256-no?authuser=0",
                                "action": {
                                    "type": "postback",
                                    "label": "風俗",
                                    "data": "風俗_表示",
                                    "displayText": "行きたい風俗を表示",
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
