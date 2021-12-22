import inspect

import fastapi
import uvicorn


from unimatrix.ext import webapi


app = webapi.Service(
    allowed_hosts=['*'],
    enable_debug_endpoints=True
)


def f(foo: int, bar: int):
    pass


class RequestHandler:

    @property
    def __signature__(self):
        return inspect.signature(f)

    async def __call__(self):
        pass


handler = RequestHandler()
app.add_api_route('/', handler)


if __name__ == '__main__':
    uvicorn.run(app,
        host="127.0.0.1",
        port=5000,
        log_level="info"
    )
