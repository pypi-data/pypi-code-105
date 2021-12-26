class RoomNotFound(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class InvalidUser(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class InvalidRoom(Exception):
    def __init__(self, mesage: str) -> None:
        super().__init__(mesage)

class UserNotInRoom(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class BannedUser(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class UserDisabled(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

class Unknown(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)