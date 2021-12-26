from ujson import loads

class RocketResponse:
    def __init__(self, status: int, body: str) -> None:
        jsonBody: dict = loads(body)
        self._isAuth: bool = False
        self.status: int = status
        self.body: str = body
        self.isSucceed: bool
        self.error: str = None
        self.errorType: str = None
        if "status" in jsonBody.keys():
            self._isAuth = True
        if not self._isAuth:
            self.isSucceed = jsonBody["success"]
            if not self.isSucceed:
                self.isSucceed = False
                self.error = jsonBody["error"]
                self.errorType = jsonBody["errorType"]
        else:
            if self.status == 200:
                self.isSucceed = True
            else:
                self.isSucceed = False
                self.error = jsonBody["message"]
                self.errorType = jsonBody["error"]
