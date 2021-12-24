import inspect

import fastapi
import uvicorn

import ioc
from unimatrix.ext import webapi


app = webapi.Service(
    allowed_hosts=['*'],
    enable_debug_endpoints=True
)


class BookRepository:
    DoesNotExist = type('Exception', (Exception,), {})

    async def transfer(self, *args, **kwargs):
        return {'title': "Homerus"}

ioc.provide('BookRepository', BookRepository)


async def f(request: fastapi.Request, foo: int, bar: int, book=webapi.CurrentEntity('BookRepository')):
    raise Exception


class RequestHandler:

    @property
    def __signature__(self):
        return inspect.signature(f)

    @classmethod
    def as_endpoint(cls):
        handler = cls()
        async def request_handler(*args, **kwargs):
            return await handler(*args, **kwargs)
        request_handler.__signature__ = handler.__signature__
        return request_handler

    async def handle(self, request: fastapi.Request, *args, **kwargs):
        return kwargs.get('book')

    async def __call__(self, *args, **kwargs):
        return await self.handle(*args, **kwargs)

handler = RequestHandler()
app.add_api_route('/{foo:int}', handler.as_endpoint(), methods=['GET','POST'])


if __name__ == '__main__':
    uvicorn.run(app,
        host="127.0.0.1",
        port=5000,
        log_level="info"
    )
