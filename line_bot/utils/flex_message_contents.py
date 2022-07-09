# dict_sample = {
#     "type": "carousel",
#     "contents": ["contents"]
#     }

# place_name = ["平成女学院", "女~磐線"]
# url_name = ["jogakuin.com", "jobansen.com"]

#image,place,urlを代入してdictを返却
#それを元に配列にappendしてcontentsを作成
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
    contents["body"]["contents"]["text"] = place_name
    contents["footer"]["contents"]["uri"] = url_name
    
    return contents

#最終的なcontents作成
def make_flex_contents(contents_list):
    contents = {
    "type": "carousel",
    "contents": contents_list
    }
    return contents