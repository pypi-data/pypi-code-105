from types import FunctionType
from typing import Optional
from ujson import loads
from uuid import uuid4 as uid
from .httpclient import HttpClient
from .pkg.objects.account import Account
from .pkg.exceptions.utils import findException
from .pkg.exceptions.rocket.utils import findRocketException
from .pkg.objects.response import APIResponse
from .pkg.objects.rocketresponse import RocketResponse
from .pkg.exceptions.exceptionlist import Unauthorized
from .pkg.utils.objectification import composeChannel
from .pkg.utils.objectification import composeRoom
from .pkg.utils.objectification import composeComment
from .pkg.utils.objectification import composeMessage
from .pkg.utils.objectification import composePostList
from .pkg.utils.objectification import composeSuggestedChannelList
from .pkg.objects.postlist import PostList
from .pkg.objects.post import Post
from .pkg.objects.rocket.room import Room
from .pkg.objects.comment import Comment
from .pkg.objects.rocket.message import Message
from .pkg.objects.rocket.channel import Channel
from .pkg.objects.rocket.suggestedchannel import SuggestedChannel
from .chatsocket import ChatSocket
from .lib.postsearch import *

class AnonClient(HttpClient):
    def __init__(self) -> None:
        super().__init__()
        self._socketInstance: ChatSocket = None
        self._socketRequired: bool = False
        self._session: Account = None

    def getSession(self) -> Optional[Account]:

        """
        If authorization has been performed, returns Account instance.
        In other cases, returns None
        """

        return self._session

    async def _rocketAuth(self, login: str, key: str) -> tuple:
        data: dict = {
            "username": login,
            "password": key
        }
        result: RocketResponse = await self.rocketPost("login", data)
        data: dict = loads(result.body)["data"]
        userId = data["userId"]
        rocketToken = data["authToken"]
        return (userId, rocketToken)

    async def auth(self, login: str, password: str) -> Account:

        """
        Login to an existing account. 
        On success, sets authorization tokens in the headerы and returns Account instance
        """

        data: dict = {
            "login": login,
            "password": password
        }
        result: APIResponse = await self.post("auth/login", data)
        if result.isSucceed:
            responseData: dict = loads(result.body)["data"]
            account: Account = Account(
                responseData["login"],
                password,
                responseData["id"],
                responseData["email"],
                responseData["rocketId"],
                responseData["rocketKey"],
                responseData["isDisabled"],
                responseData["isGcmMissing"],
                responseData["level"],
                responseData["token"]
            )
            rocketId, rocketToken = await self._rocketAuth(login, account.rocketKey)
            account.rocketId = rocketId
            account.rocketToken = rocketToken
            self._session = account
            if self._socketRequired:
                if self._socketInstance and self._socketInstance.authorized:
                    await self._socketInstance.stop()
                    self._socketInstance = ChatSocket.start(rocketToken, rocketId)
                elif self._socketInstance and not self._socketInstance.authorized:
                    await self._socketInstance.auth(rocketToken, rocketId)
                else:
                    self._socketInstance = ChatSocket.start(rocketToken, rocketId)
            self.setSession(account)
            return account
        raise findException(result.code, result.message)

    async def register(self, login: str, name: str, password: str, setCredentials: bool = True) -> Account:

        """
        Creates a new account.
        On success, returns Account instance
        """

        data: dict = {
            "login": login,
            "name": name,
            "password": password
        }
        result: APIResponse = await self.post("auth/register", data)
        if result.isSucceed:
            responseData: dict = loads(result.body)["data"]
            account: Account = Account(
                responseData["login"],
                password,
                responseData["id"],
                responseData["email"],
                responseData["rocketId"],
                responseData["rocketKey"],
                responseData["isDisabled"],
                responseData["isGcmMissing"],
                responseData["level"],
                responseData["token"]
            )
            rocketId, rocketToken = await self._rocketAuth(login, account.rocketKey)
            account.rocketId = rocketId
            account.rocketToken = rocketToken
            if setCredentials:
                self._session = account
                if self._socketRequired:
                    if self._socketInstance and self._socketInstance.authorized:
                        await self._socketInstance.stop()
                        self._socketInstance = ChatSocket.start(rocketToken, rocketId)
                    elif self._socketInstance and not self._socketInstance.authorized:
                        await self._socketInstance.auth(rocketToken, rocketId)
                    else:
                        self._socketInstance = ChatSocket.start(rocketToken, rocketId)
                self.setSession(account)
            return account
        raise findException(result.code, result.message)
    
    async def getPosts(self, filter: str = MY_MIX, size: int = 20, after: str = None, periodOfTime: str = None) -> list[Post]:

        """
        Gets posts in the feed. 
        On success, returns PostList (list extension) instance
        """

        if not self._session:
            raise Unauthorized()
        url: str
        if after:
            url = f"posts/v1/main?filter={filter}&first={size}&after={after}"
        else:
            url = f"posts/v1/main?filter={filter}&first={size}"
        if periodOfTime:
            url = url + f"&periodOfTime={periodOfTime}"
        result: APIResponse = await self.get(url)
        if result.isSucceed:
            json: dict = loads(result.body)["data"]
            array: list = json["items"]
            cursor: str = json["cursor"]
            return composePostList(array, cursor)
        raise findException(result.code, result.message)
    
    async def chatRequest(self, userId: str, requestContent: str) -> None:

        """
        Sends a request to start a dialog.
        """

        if not self._session:
            raise Unauthorized()
        data: dict = {
            "greeting": requestContent
        }
        result: APIResponse = await self.post(f"users/{userId}/chat-request", data)
        if not result.isSucceed:
            raise findException(result.code, result.message)
    
    async def startChat(self, **kwargs) -> Room:

        """
        Creates a new chat without a request for it. 
        Can take (rocket) username or (rocket) user ID as arguments.
        In addition, optional: text of the first message
        On success, returns Room instance
        """

        if len(kwargs) != 1 :
            raise TypeError("Invalid arguments")
        if "username" not in kwargs and "rocketId" not in kwargs:
            raise TypeError("Invalid arguments")
        if not self._session:
            raise Unauthorized()
        initialMessage: str = None
        if "text" in kwargs:
            initialMessage = kwargs["text"]
        data: dict
        if "username" in kwargs:
            data = {
                "username": kwargs["username"]
            }
        elif "rocketId" in kwargs:
            data = {
                "userId": kwargs["rocketId"]
            }
        result: RocketResponse = await self.rocketPost("im.create", data)
        if result.isSucceed:
            roomJson: dict = loads(result.body)["room"]
            room: Room = composeRoom(roomJson)
            if initialMessage:
                self.sendMessage(room.id, initialMessage)
            return room
        raise findRocketException(result.error, result.errorType)
    
    async def comment(self, postId: str, content: str) -> Comment:

        """
        Creates a new comment. 
        On success, returns Comment instance
        """

        if not self._session:
            raise Unauthorized()
        data: dict = {
            "contents": [{
                "data": {
                    "value": content
                },
                "type": "TEXT"
            }],
            "isAuthorHidden": False,
            "parentId": postId
        }
        result: APIResponse = await self.post(f"posts/v1/comments", data)
        if result.isSucceed:
            comment: dict = loads(result.body)["data"]["comment"]
            return composeComment(comment)
        raise findException(result.code, result.message)
    
    async def sendMessage(self, roomId: str, text: str) -> Message:

        """
        Sends a message to the chat.
        On success, returns Message instance
        """

        if not self._session:
            raise Unauthorized()
        data: dict = {
            "message": {
                "_id": str(uid()),
                "rid": roomId,
                "msg": text
            }
        }
        result: RocketResponse = await self.rocketPost("chat.sendMessage", data)
        if result.isSucceed:
            message: dict = loads(result.body)["message"]
            return composeMessage(message)
        raise findRocketException(result.error, result.errorType)
    
    async def joinChannel(self, roomId: str) -> Channel:

        """
        Joins the channel.
        On success, returns Channel instance
        """
        
        if not self._session:
            raise Unauthorized()
        data: dict = {
            "roomId": roomId
        }
        result: RocketResponse = await self.rocketPost("channels.join", data)
        if result.isSucceed:
            channel: dict = loads(result.body)["channel"]
            return composeChannel(channel)
        raise findRocketException(result.error, result.errorType)
    
    async def leaveChannel(self, roomId: str) -> Channel:

        """
        Leaves the channel.
        On success, returns Channel instance
        """

        if not self._session:
            raise Unauthorized()
        data: dict = {
            "roomId": roomId
        }
        result: RocketResponse = await self.rocketPost("channels.leave", data)
        if result.isSucceed:
            channel: dict = loads(result.body)["channel"]
            return composeChannel(channel)
        raise findRocketException(result.error, result.errorType)

    async def getSuggestedChannels(self) -> list[SuggestedChannel]:

        """
        Returns a list of suggested channels.
        """

        if not self._session:
            raise Unauthorized()
        result: RocketResponse = await self.rocketGet("channels.list.suggestions")
        if result.isSucceed:
            array: list = loads(result.body)["channels"]
            return composeSuggestedChannelList(array)
        raise findRocketException(result.error, result.errorType)
    
    def onChatMessage(self, listener: FunctionType):
        if not self._socketRequired:
            self._socketRequired = True
            self._socketInstance = ChatSocket.start()
        self._socketInstance.addListener("chatMessage", listener)