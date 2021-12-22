import asyncio, typing

class Result():
    def __init__(self, result : str):
        self.result : str = result

class Set():
    def __init__(self, query : str):
        self.query : str = query
            
class Get():
    def __init__(self, query : str):
        self.query : str = query

class Query():
    def __init__(self, connection):
        self.reader = connection.reader
        self.writer = connection.writer
        
    async def do_query(protocol : typing.Union[Get, Set]):
        self.writer.write(protocol.query.encode())
        await self.writer.drain()
        data = await self.reader.read(100)
        return Result(f'{data.decode()!r}')
    
