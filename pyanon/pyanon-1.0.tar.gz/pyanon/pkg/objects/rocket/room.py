class Room:
    def __init__(self,
                id: str,
                messagesCount: int,
                createdTimestamp: str,
                updatedTimestamp: str,
                usernames: list[str]):
        self.id: str = id
        self.messagesCount: int = messagesCount
        self.createdTimestamp: str = createdTimestamp
        self.updatedTimestamp: str = updatedTimestamp
        self.usernames: list[str] = usernames