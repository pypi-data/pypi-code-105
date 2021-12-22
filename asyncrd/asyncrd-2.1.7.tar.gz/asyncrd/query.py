import asyncio, typing
from .exceptions import CatchException, RedisException

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
        
    async def do_query(self, protocol : typing.Union[Get, Set]):
        data_ = protocol.query+"\r\n"
        self.writer.write(data_.encode())
        await self.writer.drain()
        data = await self.reader.read(100)
        res = Result(data.decode('utf-8'))
        res = res.result
        res = res.replace("\r", "")
        res = res.replace("\n", "")
        catching = CatchException(text=res)
        await catching.catch_error()
        return res
    
