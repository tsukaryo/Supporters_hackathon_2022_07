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
def make_class_CS_reply_register(reply_token,items_list):
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


class CS_reply_register(): 
    def __init__(self):
        self.items_list = []
        self.body= {}
    
    def make_item_list(self, category_name):
        item = make_category_item(category_name)
        self.item_list.append(item)
        return 0
    
    def reply(self):
        self.body = make_class_CS_reply_register(self.items_list)
        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(self.body).encode(), HEADER)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)
        return 0




def make_category_item(category_name):
    item = {
            "type": "action",
            "imageUrl": "https://lh3.googleusercontent.com/pw/AM-JKLWxIgFi1YDBcB85CcFkwsA9ZJEgZg-l8jw_s3qy0pAcb11XLKKrqyh9yaepyb3wDbvzMuWJi44LctXHjJQ7GjFGbyYD0xcd6Wgeev3Tjb-O6evGBRFknQJ0oBFk4ZnsW7xfNkkXYxnHA3QpkRg71Pu7nA=s256-no?authuser=0",
            "action": {
                "type": "postback",
                "label": "",#ここをcategory_nameで作成
                "data": "",#ここをcategory_nameで作成
                "displayText": "",#ここをcategory_nameで作成
            }
        }

    item["action"]["label"] = category_name
    item["action"]["data"] = category_name 
    item["action"]["displayText"] = category_name
    return item

#最終的なcontents作成
def make_quick_category_body(reply_token,item_list):
    body = {
        'replyToken': reply_token,
            "messages":[
                {
                    "type": "text",
                    "text": "カテゴリーを選択してね",
                    "quickReply":{
                        "items": 
                            item_list
                    }
                }
            ]
        }
    return body


class Category_register(): 
    def __init__(self):
        self.item_list = []
        self.body= {}
        self.all_item = {
            "type": "action",
            "imageUrl": "https://lh3.googleusercontent.com/pw/AM-JKLUcVu6uzRhfdsJ5_-S8FueUWdiFfzrhs4sJ5trdGjIA8OtO_uj5-N6XIh-TA7vDNCbddEYFQlt5QmHnorCEdXbIcG4R0WaCx19wvPocI1fuwlfZXNJodvDY0ysBw7sTvUqmweX-jV-ukVn5iU2SMB0WQQ=s256-no?authuser=0",
            "action": {
                "type": "postback",
                "label": "ALL",#ここをcategory_nameで作成
                "data": "ALL",#ここをcategory_nameで作成
                "displayText": "全て",#ここをcategory_nameで作成
            }
        }

        self.item_list.append(self.all_item)

    def make_item_list(self, category_name):
        item = make_category_item(category_name)
        self.item_list.append(item)
        return 0

    def reply(self, reply_token):
        self.body = make_quick_category_body(reply_token,self.item_list)
        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(self.body).encode(), HEADER)
        try:
            with urllib.request.urlopen(req) as res:
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)
        return 0