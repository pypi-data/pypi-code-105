from typing import Optional
from .pictures import Pictures

class User:
    def __init__(self, id: str, name: str, photo: Optional[Pictures], banner: Optional[Pictures]) -> None:
        self.id: str = id
        self.name: str = name
        self.photo: Optional[Pictures] = photo
        self.banner: Optional[Pictures] = banner