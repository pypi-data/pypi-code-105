from .picture import Picture
from typing import Optional

class Pictures:
    def __init__(self,
                type: str,
                id: str,
                extraSmall: Optional[Picture],
                small: Optional[Picture],
                medium: Optional[Picture],
                large: Optional[Picture],
                extraLarge: Optional[Picture],
                original: Optional[Picture]) -> None:
        self.type: str = type
        self.id: str = id
        self.extraSmall: Optional[Picture] = extraSmall
        self.small: Optional[Picture] = small
        self.medium: Optional[Picture] = medium
        self.large: Optional[Picture] = large
        self.extraLarge: Optional[Picture] = extraLarge
        self.original: Optional[Picture] = original