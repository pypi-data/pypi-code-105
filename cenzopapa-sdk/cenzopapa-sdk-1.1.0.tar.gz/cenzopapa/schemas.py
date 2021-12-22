import datetime
from dataclasses import dataclass


@dataclass
class Image:
    id: int
    url: str
    width: int
    height: int
    posted_at: datetime.datetime


@dataclass
class ImageList:
    count: int
    next: str
    previous: str
    results: list[Image]
