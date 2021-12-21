"""
pyazureutils specific exceptions
"""

class PyazureutilsError(Exception):
    """Base class for all pyazureutils specific exceptions"""
    def __init__(self, msg=None, code=0):
        super().__init__(msg)
        self.code = code

class ApplicationError(PyazureutilsError):
    """Error connecting to Azure application"""
    def __init__(self, msg=None, code=0):
        super().__init__(msg, code)

class AzureConnectionError(PyazureutilsError):
    """Unable to connect"""
    def __init__(self, msg=None, code=0):
        super().__init__(msg, code)

class KitConnectionError(PyazureutilsError):
    """Unable to connect"""
    def __init__(self, msg=None, code=0):
        super().__init__(msg, code)

class DeviceTemplateError(PyazureutilsError):
    """Error with device template"""
    def __init__(self, msg=None, code=0):
        super().__init__(msg, code)

class RestApiError(PyazureutilsError):
    """Error when making REST API call"""
    def __init__(self, msg=None, code=0):
        super().__init__(msg, code)