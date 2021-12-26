from .coordinates import Coordinates
from .pictures import Pictures
from .user import User
from .page import Page
from typing import Optional

class Post:
    def __init__(self,
                id: str,
                isCreatedByPage: Optional[bool],
                status: str,
                type: str,
                coordinates: Optional[Coordinates],
                isCommentable: bool,
                hasAdultContent: bool,
                isAuthorHidden: bool,
                photo: Optional[Pictures],
                content: Optional[str],
                author: Optional[User],
                page: Optional[Page]) -> None:
        self.id: str = id
        self.isCreatedByPage: Optional[bool] = isCreatedByPage
        self.status: str = status
        self.type: str = type
        self.coordinates: Optional[Coordinates] = coordinates
        self.isCommentable: bool = isCommentable
        self.hasAdultContent: bool = hasAdultContent
        self.isAuthorHidden = isAuthorHidden
        self.photo: Optional[Pictures] = photo
        self.content: Optional[str] = content
        self.author: Optional[User] = author
        self.page: Optional[Page] = page