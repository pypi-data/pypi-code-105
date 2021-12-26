class RocketEvent:
    def __init__(self, msg: str, collection: str, id: str) -> None:
        self.msg: str = msg
        self.collection: str = collection
        self.id: str = id