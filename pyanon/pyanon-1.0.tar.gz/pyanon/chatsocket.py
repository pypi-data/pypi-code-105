import asyncio
from threading import Thread
from .pkg.utils.headers import HeadersUtils
from websockets import connect
from websockets import WebSocketClientProtocol
from ujson import dumps
from ujson import loads
from .pkg.objects.rocket.message import Message
from .lib.rocket.notification import Notification
from .pkg.utils.objectification import composeNotification
from types import FunctionType

class ChatSocket:

    notificationListener: FunctionType = None
    subscriptionsChangingListener: FunctionType = None
    roomsChangingListener: FunctionType = None

    def __init__(self, rocketToken: str = None, rocketId: str = None) -> None:
        self.socketEndpoint: str = "wss://rocketchat.anonym.network/websocket"
        self.token: str = rocketToken
        self.id: str = rocketId
        self.authorized: bool = False
        if self.token:
            self.authorized = True
        self.disconnectRequested: bool = False
        self.ws: WebSocketClientProtocol = None

    async def _handle(self, message: dict):
        try: name: str = message["fields"]["eventName"].split("/")[1]
        except KeyError: return
        if self.authorized:
            if name == "notification":
                if self.__class__.notificationListener:
                    notification: Notification = composeNotification(message)
                    await self.__class__.notificationListener(notification)

    async def _auth(self, ws):
        data: str = dumps({
            "msg": "connect",
            "version": "1",
            "support": [
                "1",
                "pre2",
                "pre1"
            ]
        })
        await ws.send(data)
        data: str = dumps({
            "msg": "method",
            "id": "2",
            "method": "login",
            "params": [
                {
                "resume": self.token
                }
            ]
        })
        await ws.send(data)
        data: str = dumps({
            "msg": "sub",
            "id": "5",
            "name": "stream-notify-user",
            "params": [
                f"{self.id}/notification",
                False
            ]
        })
        await ws.send(data)

    async def _connect(self):
        connection: WebSocketClientProtocol = await connect(self.socketEndpoint)
        self.ws = connection
        if self.authorized: await self._auth(connection)
        while True:
            msg: str = await connection.recv()
            json = loads(msg)
            try: 
                if json["msg"] == "ping": await connection.send(dumps({"msg": "pong"}))
                else: await self._handle(json)
            except KeyError:
                await self._handle(json)

    def _run(self):
        loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._connect())
        loop.run_forever()
    
    def addListener(self, listenerType: str, listener: FunctionType):
        if listenerType == "chatMessage":
            self.__class__.notificationListener = listener
        elif listenerType == "subscriptions":
            self.__class__.subscriptionsChangingListener = listener
        elif listenerType == "rooms":
            self.__class__.roomsChangingListener = listener

    async def stop(self):
        self.token = None
        self.id = None
        self.authorized = False
        await self.ws.close()

    async def auth(self, rocketToken: str, rocketId: str):
        self.token = rocketToken
        self.id = rocketId
        self.authorized = True
        await self._auth(self.ws)

    @classmethod
    def start(cls, rocketToken: str = None, rocketId: str = None):
        instance: ChatSocket = cls(rocketToken, rocketId)
        t = Thread(target = instance._run)
        t.start()
        t.join(0.1)
        return instance