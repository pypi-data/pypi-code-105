from .rocketexceptions import *

def findRocketException(error: str, errorType: str) -> Exception:
    if errorType == "error-invalid-user": return InvalidUser(error)
    elif errorType == "error-room-not-found": return RoomNotFound(error)
    elif errorType == "error-invalid-room": return InvalidRoom(error)
    elif errorType == "error-user-not-in-room": return UserNotInRoom(error)
    elif errorType == "error-banned-user": return BannedUser(error)
    elif errorType == "error-user-disabled": return UserDisabled(error)
    else: return Unknown(error)