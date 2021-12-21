from time import time
from ujson import loads
from base64 import b64decode
from functools import reduce
from aiohttp import ClientSession
from requests import Session

session = Session()
ED_API = "https://ed-server.herokuapp.com/api"


def generate_device(data: str = time()) -> str:
    response = session.get(f"{ED_API}/generator/ndcdeviceid?data={str(data)}")
    return response.json()["message"]
    

async def _generate_signature(session: ClientSession, data: str) -> str:
    response = await session.get(f"{ED_API}/generator/ndc-msg-sig?data={str(data)}")
    return (await response.json(content_type=None))["message"]


def get_timers(size: int) -> list[dict[str, int]]:
    return tuple(map(lambda _: {"start": int(time()), "end": int(time() + 300)}, range(size)))


def decode_sid(sid: str) -> dict:
    args = (lambda a, e: a.replace(*e), ("-+", "_/"), sid+"="*(-len(sid) % 4))
    return loads(b64decode(reduce(*args).encode())[1:-20].decode())


def sid_to_uid(sid: str) -> str:
    return decode_sid(sid)["2"]


def sid_to_ip_address(sid: str) -> str:
    return decode_sid(sid)["4"]
