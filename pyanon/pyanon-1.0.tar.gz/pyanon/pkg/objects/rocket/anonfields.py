class AnonFields:
    def __init__(self,
                anonId: str,
                photoUrl: str,
                registeredTimestamp: int) -> None:
        self.anonId: str = anonId
        self.photoUrl: str = photoUrl
        self.registeredTimestamp: int = registeredTimestamp 