from typing import Any

import orjson
import uvicorn
from starlette.responses import JSONResponse


class OrjsonResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)


class Handler:
    def __init__(self, actor):
        self.provided_actor = actor

    async def __call__(self, scope, receive, send):
        assert scope["type"] == "http"
        content = await self.provided_actor({"http": {}})
        response = OrjsonResponse(content)
        await response(scope, receive, send)


def start(actor):
    u_handler = Handler(actor)
    uvicorn.run(u_handler, host="0.0.0.0", port=5000, log_level="warning")
