from .pictures import Pictures
from typing import Optional

class Page:
    def __init__(self, 
                id: str, 
                type: str, 
                status: str, 
                ownedBy: str, 
                title: str, 
                description: str, 
                photo: Optional[Pictures], 
                banner: Optional[Pictures]):
        self.id: str = id
        self.type: str = type
        self.status: str = status
        self.ownedBy: str = ownedBy
        self.title: str = title
        self.description: str = description
        self.photo: Optional[Pictures] = photo
        self.banner: Optional[Pictures] = banner