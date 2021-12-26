import os

try:
    import requests
except:
    os.system("pip install requests")
    import requests

version = "v2"

async def bot_name(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/bots/{id}").json()
    try:
        bots = req['data']['name']
    except:
        print("\n한국 봇리스트에 없는 봇이에요! \nThis bot is not on the Korean bot list!")
        return
    return bots

async def bot_id(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/bots/{id}").json()
    try:
        bots = req['data']['id']
    except:
        print("\n한국 봇리스트에 없는 봇이에요! \n This bot is not on the Korean bot list!")
        return
    return bots

async def bot_tag(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/bots/{id}").json()
    try:
        bots = req['data']['tag']
    except:
        print("\n한국 봇리스트에 없는 봇이에요! \nThis bot is not on the Korean bot list!")
        return
    return bots

async def bot_owners(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/bots/{id}").json()
    try:
        users = []
        for bot in req['data']['owners']:
            users.append(f"{bot['username']}#{bot['tag']}")
    except:
        print("\n한국 봇리스트에 없는 봇이에요! \nThis bot is not on the Korean bot list!")
        return
    return users

async def bot_category(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/bots/{id}").json()
    try:
        bots = req['data']['category']
    except:
        print("\n한국 봇리스트에 없는 봇이에요! \nThis bot is not on the Korean bot list!")
        return
    return bots

async def bot_bg(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/bots/{id}").json()
    try:
        bots = req['data']['bg']
    except:
        print("\n한국 봇리스트에 없는 봇이에요! \nThis bot is not on the Korean bot list!")
        return
    return bots

async def bot_banner(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/bots/{id}").json()
    try:
        bots = req['data']['banner']
    except:
        print("\n한국 봇리스트에 없는 봇이에요! \nThis bot is not on the Korean bot list!")
        return
    return bots

async def bot_status(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/bots/{id}").json()
    try:
        bots = req['data']['status']
    except:
        print("\n한국 봇리스트에 없는 봇이에요! \nThis bot is not on the Korean bot list!")
        return
    return bots

async def bot_discord(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/bots/{id}").json()
    try:
        bots = f"https://discord.gg/{req['data']['discord']}"
    except:
        print("\n한국 봇리스트에 없는 봇이에요! \nThis bot is not on the Korean bot list!")
        return
    return bots

async def bot_url(id = None):
    req = requests.get(f"https://koreanbots.dev/api/{version}/bots/{id}").json()
    try:
        bots = req['data']['url']
    except:
        print("\n한국 봇리스트에 없는 봇이에요! \nThis bot is not on the Korean bot list!")
        return
    return bots