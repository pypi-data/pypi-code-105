import os

try:
    import requests
except:
    os.system("pip install requests")
    import requests

version = "v2"

async def user_name(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        users = req['data']['username']
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return users

async def user_id(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        users = req['data']['id']
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return users

async def user_git(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        users = req['data']['github']
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return users

async def user_tag(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        users = req['data']['tag']
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return users

async def user_flags(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        users = req['data']['flags']
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return users

#------------------------------------------------------------------------------------------------------------

async def user_bot_name(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        bots = []
        for bot in req['data']['bots']:
            bots.append(str(bot['name']))
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return bots

async def user_bot_url(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        bots = []
        for bot in req['data']['bots']:
            bots.append(str(bot['url']))
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return bots

async def user_bot_desc(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        bots = []
        for bot in req['data']['bots']:
            bots.append(str(bot['desc']))
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return bots

async def user_bot_id(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        bots = []
        for bot in req['data']['bots']:
            bots.append(str(bot['id']))
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return bots

async def user_bot_discord(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        bots = []
        for bot in req['data']['bots']:
            bots.append("https://discord.gg/"+str(bot['discord']))
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return bots

async def user_bot_intro(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        bots = []
        for bot in req['data']['bots']:
            bots.append(str(bot['intro']))
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return bots

async def user_bot_status(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        bots = []
        for bot in req['data']['bots']:
            bots.append(str(bot['status']))
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return bots

async def user_bot_category(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        bots = []
        for bot in req['data']['bots']:
            bots.append(str(bot['category']))
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return bots

async def user_bot_bg(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        bots = []
        for bot in req['data']['bots']:
            bots.append(str(bot['bg']))
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return bots

async def user_bot_banner(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        bots = []
        for bot in req['data']['bots']:
            bots.append(str(bot['banner']))
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return bots

async def user_bot_lib(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        bots = []
        for bot in req['data']['bots']:
            bots.append(str(bot['lib']))
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return bots

async def user_bot_tag(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        bots = []
        for bot in req['data']['bots']:
            bots.append(str(bot['tag']))
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return bots

async def user_bot_git(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        bots = []
        for bot in req['data']['bots']:
            bots.append(str(bot['git']))
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return bots

async def user_bot_web(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        bots = []
        for bot in req['data']['bots']:
            bots.append(str(bot['web']))
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return bots

async def user_bot_prefix(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/users/{id}").json()
    try:
        bots = []
        for bot in req['data']['bots']:
            bots.append(str(bot['prefix']))
    except:
        print("한국 봇리스트에 없는 유저에요! \n A user who is not on the Korean bot list!")
        return
    return bots