class Unspecified(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class Validation(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class Flood(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class DailyLimitReached(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class NotEnoughWritePermissions(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class Unknown(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class Unauthorized(Exception):
    def __init__(self) -> None:
        super().__init__("You must login to do this")