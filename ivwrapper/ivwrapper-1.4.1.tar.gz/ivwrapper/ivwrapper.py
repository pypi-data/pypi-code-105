from aiohttp import request


class Api:
    def __init__(self):
        self.url = "https://ivall.pl/"

    async def get_joke(self):
        async with request(method="GET", url=self.url + "zart") as r:
            r = (await r.json())["url"]

        return r.strip()

    async def get_meme(self):
        async with request(method="GET", url=self.url + "memy") as r:
            r = (await r.json())["url"]

        return r
