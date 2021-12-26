from .exceptionlist import *

def findException(code: str, message: str) -> Exception:
    if code == "UNSPECIFIED": return Unspecified(message)
    elif code == "VALIDATION": return Validation(message)
    elif code == "FLOOD": return Flood(message)
    elif code == "LIMIT_REACHED": return DailyLimitReached(message)
    elif code == "COMMENT_NOT_ENOUGH_WRITE_PERMISSIONS": return NotEnoughWritePermissions(message)
    else: return Unknown(message)