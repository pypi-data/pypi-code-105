from typing import Optional


class Comment:
    def __init__(self, 
                id: str,
                content: str,
                authorId: str,
                createdTimestamp: int,
                updatedTimestamp: int,
                isAuthorHidden: bool,
                replyToCommentId: Optional[str],
                replyToAuhorId: Optional[str]) -> None:
        self.id: str = id
        self.content: str = content
        self.authorId: str = authorId
        self.createdTimestamp: int = createdTimestamp
        self.updatedTimestamp: int = updatedTimestamp
        self.isAuthorHidden: bool= isAuthorHidden
        self.replyToCommentId: Optional[str] = replyToCommentId
        self.replyToAuthorId: Optional[str] = replyToAuhorId