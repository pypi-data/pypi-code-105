from .rocketuser import RocketUser

class Message:
    def __init__(self, 
                id: str,
                content: str,
                alias: str,
                roomId: str,
                createdTimestamp: str,
                updatedTimestamp: str,
                author: RocketUser) -> None:
        self.id: str = id
        self.content: str = content
        self.alias: str = alias
        self.roomId: str = roomId
        self.createdTimestamp: str = createdTimestamp
        self.updatedTimestamp: str = updatedTimestamp
        self.author: RocketUser = author