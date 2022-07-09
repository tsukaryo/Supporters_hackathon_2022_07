# dict_sample = {
#     "type": "carousel",
#     "contents": ["contents"]
#     }

# place_name = ["平成女学院", "女~磐線"]
# url_name = ["jogakuin.com", "jobansen.com"]

# #1個ずつimage, place, urlを代入してdict型を出力
# #配列作って出力したdictをappendしてlistを下のmake_flex_messageに代入
# def make_contents(image_file, place_name, url_name):
#     contents = {
#         "type": "bubble",
#         "hero": {
#             "type": "image",
#             "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png", #ここに入れたい画像
#             "size": "full",
#             "aspectRatio": "20:13",
#             "aspectMode": "cover"
#         },
#         "body": {
#             "type": "box",
#             "layout": "horizontal",
#             "contents": [
#             {
#                 "type": "text",
#                 "text": "", #ここに場所名 ex.平成女学院
#                 "size": "xl",
#                 "weight": "bold",
#                 "align": "center"
#             }
#             ]
#         },
#         "footer": {
#             "type": "box",
#             "layout": "vertical",
#             "contents": [
#             {
#                 "type": "button",
#                 "action": {
#                 "type": "uri",
#                 "label": "WEBSITE",
#                 "uri": "" #ここにURL
#                 }
#             }
#             ]
#         }
#     }
#     contents["hero"]["url"] = image_file
#     contents["body"]["contents"]["text"] = place_name
#     contents["footer"]["contents"]["uri"] = url_name
    
#     return contents #dict

# #json作成
# def make_flex_messages(contents_list):
#     flex_messages_json = {
#     "type": "carousel",
#     "contents": contents_list
#     }
#     return flex_messages_json