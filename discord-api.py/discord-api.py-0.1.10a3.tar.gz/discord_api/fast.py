import asyncio

def setup_fast(client):
    try:
        import uvloop
    except ImportError:
        pass
    if not isinstance(asyncio.get_event_loop_policy(), uvloop.EventLoopPolicy):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    try:
        import ujson
    except ImportError:
        client.json = json
    else: 
        client.json = ujson
