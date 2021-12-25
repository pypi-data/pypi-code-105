class ReaderRbvException(Exception):
    pass


class Unreachable(ReaderRbvException):
    pass


class InvalidCredential(ReaderRbvException):
    pass


class BookNotFound(ReaderRbvException):
    pass


class BookSectionNotFound(ReaderRbvException):
    pass


class GetImageFailed(ReaderRbvException):
    pass


class LoginFailed(ReaderRbvException):
    pass
