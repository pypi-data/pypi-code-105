from beetools import msg_error


class PackageItException(Exception):
    """
    Error handling in PackageIt is done with exceptions. This class is the base of all exceptions raised by PackageIt
    Some other types of exceptions might be raised by underlying libraries.
    """

    def __init__(self, status, data):
        super().__init__()
        self.__code = status[0]
        self.__data = data
        self.__title = status[1]
        print(msg_error(f"{self.__code}:{self.__title}"))
        print(msg_error("\n".join(self.__data)))

    @property
    def code(self):
        """
        The (decoded) data returned by the PackageIt API
        """
        return self.__code

    @property
    def data(self):
        """
        The (decoded) data returned by the PackageIt API
        """
        return self.__data

    @property
    def title(self):
        """
        The status returned by the PackageIt API
        """
        return self.__title

    def __str__(self):
        return f"{self.__code}: {self.__title}"


class OldVersionException(PackageItException):
    """
    Exception raised if the PyPI version is later or equal to the intended GitHub/PackageIt/Release.
    """
