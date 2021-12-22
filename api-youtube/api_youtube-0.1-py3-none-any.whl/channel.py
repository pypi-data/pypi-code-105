"""
Add channel_name to 'name'\n
Just add the maximum value to 'max'\n
You can find out more precisely when you add 'on' to 'ex'\n
----------------------------------------------------------------------\n
'name'에는 채널_이름을 추가하세요\n
'max' 에는 최대값을 추가하면 됩니다\n
'ex' 에는 'on' 값을 추가 했을때 더욱 정확하게 알아낼수 있습니다
"""
import os

try:
    import requests
except:
    os.system("pip install requests")
    import requests

def name(name = None , max = 1,ex = "off"):
    """
    Function to send YouTube channel name\n
    --------------------------------------\n
    유튜브 채널 이름을 보내주는 함수
    """
    req = requests.get(f"https://youtube.googleapis.com/youtube/v3/search?q={name}&part=snippet&type=channel&maxResults={str(max)}&key={token}&alt=json").json()
    items = []
    for item in sorted(req['items'] , key=lambda x:x['snippet']['publishedAt']):
        if ex == "on": 
            if name in item['snippet']['title'] :
                items.append(item['snippet']['title'])
        elif ex == "off":
            items.append(item['snippet']['title'])
        else:
            print("""
'ex' can contain only 'on' or 'off'.
--------------------------------------------
'ex' 에는 'on' 또는 'off'만이들어갈수 있습니다.
            """)
            return
    return items
        
def link(name = None , max = 1,ex = "off"):
    """
    Function to send YouTube channel link\n
    --------------------------------------\n
    유튜브 채널 링크를 보내주는 함수
    """
    req = requests.get(f"https://youtube.googleapis.com/youtube/v3/search?q={name}&part=snippet&type=channel&maxResults={max}&key={token}&alt=json").json()
    items = []
    for item in sorted(req['items'] , key=lambda x:x['snippet']['publishedAt']):
        if ex == "on": 
            if name in item['snippet']['title']:
                items.append("https://www.youtube.com/channel/{}".format(item['snippet']['channelId']))
        elif ex == "off":
            items.append("https://www.youtube.com/channel/{}".format(item['snippet']['channelId']))
        else:
            print("""
'ex' can contain only 'on' or 'off'.
--------------------------------------------
'ex' 에는 'on' 또는 'off'만이들어갈수 있습니다.
            """)
    return items

def description(name = None , max = 1,ex = "off"):
    """
    Function to send YouTube channel description\n
    --------------------------------------\n
    유튜브 채널 설명을 보내주는 함수
    """
    req = requests.get(f"https://youtube.googleapis.com/youtube/v3/search?q={name}&part=snippet&type=channel&maxResults={max}&key={token}&alt=json").json()
    items = []
    for item in sorted(req['items'] , key=lambda x:x['snippet']['publishedAt']):
        if ex == "on": 
            if name in item['snippet']['title']:
                items.append(item['snippet']['description'] + "ㅤ")
        elif ex == "off":
            items.append(item['snippet']['description'] + "ㅤ")
        else:
            print("""
'ex' can contain only 'on' or 'off'.
--------------------------------------------
'ex' 에는 'on' 또는 'off'만이들어갈수 있습니다.
            """)
            return
    return items

def img_url(name = None , max = 1,ex = "off"):
    """
    Function to send YouTube channel image link\n
    --------------------------------------\n
    유튜브 채널 이미지 링크를 보내주는 함수
    """
    req = requests.get(f"https://youtube.googleapis.com/youtube/v3/search?q={name}&part=snippet&type=channel&maxResults={max}&key={token}&alt=json").json()
    items = []
    for item in sorted(req['items'] , key=lambda x:x['snippet']['publishedAt']):
        if ex == "on": 
            if name in item['snippet']['title']:
                items.append(item['snippet']['thumbnails']['high']['url'])
        elif ex == "off":
            items.append(item['snippet']['thumbnails']['high']['url'])
        else:
            print("""
'ex' can contain only 'on' or 'off'.
--------------------------------------------
'ex' 에는 'on' 또는 'off'만이들어갈수 있습니다.
            """)
            return
    return items

def make_time(name = None , max = 1,ex = "off"):
    """
    Function to send YouTube channel creation date\n
    --------------------------------------\n
    유튜브 채널 생성일 보내주는 함수
    """
    req = requests.get(f"https://youtube.googleapis.com/youtube/v3/search?q={name}&part=snippet&type=channel&maxResults={max}&key={token}&alt=json").json()
    items = []
    for item in sorted(req['items'] , key=lambda x:x['snippet']['publishedAt']):
        if ex == "on": 
            if name in item['snippet']['title']:
                items.append(item['snippet']['publishTime'])
        elif ex == "off":
            items.append(item['snippet']['publishTime'])
        else:
            print("""
'ex' can contain only 'on' or 'off'.
--------------------------------------------
'ex' 에는 'on' 또는 'off'만이들어갈수 있습니다.
            """)
            return  
    return items

token = None

def token(tk):
    global token
    token = tk