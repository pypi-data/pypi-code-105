
class DatabaseAlert:

    def __init__(self, message, super_):
        if super_.debug:
            print('\033[91m' + message + ' | DatabaseAlert | Ignoring Alert' + '\033[0m')
        else:
            raise DatabaseError(message)


class DatabaseError(Exception):
    """Error class"""
