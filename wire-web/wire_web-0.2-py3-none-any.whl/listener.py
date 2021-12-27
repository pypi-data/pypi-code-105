import typing


class EventListener:
    def __init__(self):
        self.events: typing.List[typing.Tuple[str, typing.Coroutine]] = []

    def add(self, event, handler):
        exists: bool = len([tup for tup in self.events if tup[0] == event]) > 0
        if exists:
            return 
        self.events.append((event, handler))

    async def __call__(self, event: str):
        for event_name, handler in self.events:
            if event_name == event:
                await handler()
