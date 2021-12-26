from random import sample, randint
from string import ascii_letters
from ..objects.account import Account

class HeadersUtils:
    def __init__(self) -> None:
        self._headers: dict = {
            "Host": "api.anonym.network",
            "X-Utc-Offset": self._utcOffset(),
            "X-Device-Id": self._deviceId(),
            "Accept-Language": "en",
            "X-Device-Model": "Samsung SM-N975F",
            "X-Android-App": "3.8.1.1109",
            "X-Country-code": "RU",
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "okhttp/4.9.1"
        }
        self._rocketHeaders: dict = {
            "Host": "rocketchat.anonym.network",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "okhttp/4.9.1"
        }
    
    def _utcOffset(self) -> str:
        return str(randint(-12, 12))

    def _deviceId(self) -> str:
        return "".join(sample(ascii_letters + "0123456789", 16))
    
    def getHeaders(self) -> dict:
        return self._headers
    
    def getRocketHeaders(self) -> dict:
        return self._rocketHeaders

    def setSession(self, session: Account) -> None:
        self._headers["authorization"] = session.token
        self._rocketHeaders["x-auth-token"] = session.rocketToken
        self._rocketHeaders["x-user-id"] = session.rocketId