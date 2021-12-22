import asyncio, typing

class Result():
    result : str

class Set():
    query : str

class Get():
    query : str

class Query():
    def __init__(self, connection):
        self.reader = connection.reader
        self.writer = connection.writer
        
    async def do_query(protocol : typing.Union[Get, Set]):
        self.writer.write(protocol.query.encode())
        await self.writer.drain()
        data = await self.reader.read(100)
        return Result(f'{data.decode()!r}')
    
