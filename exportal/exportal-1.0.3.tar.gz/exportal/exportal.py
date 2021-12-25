import asyncio
from typing import Any


class ExecutionPortal:

    def __init__(self) -> None:
        self._loop = asyncio.get_event_loop()
        self._s2a_queue = asyncio.Queue()
        self._a2s_queue = asyncio.Queue()

    def pass_to_async(self, item: Any, wait: bool = True) -> None:
        if wait:
            asyncio.run_coroutine_threadsafe(self._s2a_queue.put(item), self._loop).result()
        else:
            self._loop.call_soon(self._s2a_queue.put_nowait, item)
 
    def get_from_async(self) -> Any:
        return asyncio.run_coroutine_threadsafe(self._a2s_queue.get(), self._loop).result()

    async def pass_to_sync(self, item: Any, wait: bool = True) -> None:
        if wait:
            await self._a2s_queue.put(item)
        else:
            self._a2s_queue.put_nowait(item)

    async def get_from_sync(self) -> Any:
        return await self._s2a_queue.get()
