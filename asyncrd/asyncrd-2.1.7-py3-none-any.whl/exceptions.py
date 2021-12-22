import asyncio, typing
import aioconsole

class RedisException(Exception):
    def __init__(self, message : str):
        super().__init__(message)


class CatchException():
    def __init__(self, text : str):
        self.text = text
        
    async def catch_error(self):
        if self.text.startswith("-ERR"):
            text = self.text.split("-ERR ")
            raise RedisException(text[1])
            return
        return self.text
            
        
