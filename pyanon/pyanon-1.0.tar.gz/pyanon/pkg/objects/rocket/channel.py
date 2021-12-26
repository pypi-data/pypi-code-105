from typing import Optional


class Channel:
    def __init__(self, 
                id: str,
                publicId: str,
                name: str,
                messagesCount: int,
                usersCount: int,
                createdTmestamp: str,
                updatedTimestamp: str,
                country: str,
                description: Optional[str]) -> None:
        self.id: str = id
        self.publicId: str = publicId
        self.name: str = name
        self.messagesCount: int = messagesCount
        self.usersCount: int = usersCount
        self.createdTimestamp: str = createdTmestamp
        self.updatedTimestamp: str = updatedTimestamp
        self.country: str = country
        self.description: Optional[str] = description