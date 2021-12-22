class GenericException(Exception):
    def __init__(self, http_code, message):
        self._http_code = http_code
        self._message = message

    @property
    def message(self):
        return self._message

    @property
    def http_code(self):
        return self._http_code


class BadRequestException(GenericException):
    def __init__(self, message):
        super().__init__(400, message=message)


class NotFoundException(GenericException):
    def __init__(self, http_code):
        super().__init__(404, message=http_code)
