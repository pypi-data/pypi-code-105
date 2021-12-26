from ujson import loads

class APIResponse:
    def __init__(self, status: int, body: str) -> None:
        self.status: int = status
        self.body: str = body
        self.code: int = None
        self.message: str = None
        self.isSucceed: bool
        if status == 200:
            self.isSucceed = True
        else:
            self.isSucceed = False
            error = loads(body)["errors"][0]
            self.code = error["code"]
            self.message = error["message"]
