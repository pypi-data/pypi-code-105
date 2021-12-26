from typing import Optional


class SuggestedChannel:
    def __init__(self,
                id: str,
                lastMessageTimestamp: str,
                name: str,
                messagesCount: int,
                description: Optional[str]) -> None:
        self.id: str = id
        self.lastMessageTimestamp: str = lastMessageTimestamp
        self.name: str = name
        self.messagesCount: int = messagesCount
        self.description: Optional[str] = description