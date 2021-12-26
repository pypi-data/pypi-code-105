class CasambiBtError(RuntimeError):
    pass


class NetworkNotFoundError(CasambiBtError):
    pass


class ConnectionStateError(CasambiBtError):
    pass


class BluetoothError(CasambiBtError):
    def __init__(self, key: str, msg: str, *args: object) -> None:
        self.key = key
        self.msg = msg
        super().__init__(*args)


class BluetoothNotReadyError(BluetoothError):
    pass


class ProtocolError(CasambiBtError):
    pass


class AuthenticationError(CasambiBtError):
    pass
