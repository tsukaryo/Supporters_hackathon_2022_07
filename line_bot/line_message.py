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

def make_category_item(category_name):
    item = {
        {
            "type": "action",
            "imageUrl": "https://lh3.googleusercontent.com/pw/AM-JKLUcVu6uzRhfdsJ5_-S8FueUWdiFfzrhs4sJ5trdGjIA8OtO_uj5-N6XIh-TA7vDNCbddEYFQlt5QmHnorCEdXbIcG4R0WaCx19wvPocI1fuwlfZXNJodvDY0ysBw7sTvUqmweX-jV-ukVn5iU2SMB0WQQ=s256-no?authuser=0",
            "action": {
                "type": "postback",
                "label": "",#ここをcategory_nameで作成
                "data": "",#ここをcategory_nameで作成
                "displayText": "",#ここをcategory_nameで作成
            }
        },
    }
    item["action"]["label"] = category_name
    item["action"]["data"] = category_name
    item["action"]["displayText"] = category_name
    return item

#最終的なcontents作成
def make_quick_category_body(reply_token,items_list):
    body = {
        'replyToken': reply_token,
            "messages":[
                {
                    "type": "text",
                    "text": "カテゴリーを選択してね",
                    "quickReply":{
                        "items": [
                            items_list
                        ]
                    }
                }
            ]
        }
    return body


class Category_show(): 
    def __init__(self):
        self.item_list = []
        self.body= {}
    
    def make_item_list(self, category_name):
        item = make_category_item(category_name)
        self.item_list.append(item)
        return 0
    
    def reply(self):
        self.body = make_quick_category_body(self.items_list)
        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(self.body).encode(), HEADER)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)
        return 0



class CategorySelect():
    def __init__(self) -> None:
        pass

    def create_items(category_name):
        return 0



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
                                "imageUrl": "https://lh3.googleusercontent.com/pw/AM-JKLUcVu6uzRhfdsJ5_-S8FueUWdiFfzrhs4sJ5trdGjIA8OtO_uj5-N6XIh-TA7vDNCbddEYFQlt5QmHnorCEdXbIcG4R0WaCx19wvPocI1fuwlfZXNJodvDY0ysBw7sTvUqmweX-jV-ukVn5iU2SMB0WQQ=s256-no?authuser=0",
                                "action": {
                                    "type": "postback",
                                    "label": "食事",
                                    "data": "食事",
                                    "displayText": "食事",
                                }
                            },
                            {
                                "type": "action",
                                "imageUrl": "https://lh3.googleusercontent.com/pw/AM-JKLVGwM2nrMTg5zUYen435erz8hNigWAQS-qC3RFCXtjioe3Uyy-Tna0FZt99mr-51_6XZLs9DXRi1nCYKR7gzo2s-VR4sCcXL_Q_wk-mXnTtmJN6OLQUGzaKGUpdyoU9Es55rIFXhOVCGUMSFJKl-wBGgA=s256-no?authuser=0",
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
                                "imageUrl": "https://lh3.googleusercontent.com/pw/AM-JKLUcVu6uzRhfdsJ5_-S8FueUWdiFfzrhs4sJ5trdGjIA8OtO_uj5-N6XIh-TA7vDNCbddEYFQlt5QmHnorCEdXbIcG4R0WaCx19wvPocI1fuwlfZXNJodvDY0ysBw7sTvUqmweX-jV-ukVn5iU2SMB0WQQ=s256-no?authuser=0",
                                "action": {
                                    "type": "postback",
                                    "label": "食事",
                                    "data": "食事_表示",
                                    "displayText": "食べに行きたいお店を表示",
                                }
                            },
                            {
                                "type": "action",
                                "imageUrl": "https://lh3.googleusercontent.com/pw/AM-JKLVGwM2nrMTg5zUYen435erz8hNigWAQS-qC3RFCXtjioe3Uyy-Tna0FZt99mr-51_6XZLs9DXRi1nCYKR7gzo2s-VR4sCcXL_Q_wk-mXnTtmJN6OLQUGzaKGUpdyoU9Es55rIFXhOVCGUMSFJKl-wBGgA=s256-no?authuser=0",
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
                            },
                            {
                                "type": "action",
                                "imageUrl": "https://lh3.googleusercontent.com/pw/AM-JKLU1ynaba5Q3CYU6agvGQBL4quiz191SP_QyWrxa4sdZC8tft_UJYnHDYekAsN0rh3bdlxQHiwGvdox6kKIvh1gYvTdTK1zZLZrAxNDbHvvEKo5KpxVSwNqVt2hzjam63zT-skVGv77xvUQ-4UKzWamu_Q=s256-no?authuser=0",
                                "action": {
                                    "type": "postback",
                                    "label": "全て",
                                    "data": "ALL_表示",
                                    "displayText": "全てのカテゴリーを表示",
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



