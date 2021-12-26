from .picturesize import PictureSize

class Picture:
    def __init__(self, url: str, size: PictureSize) -> None:
        self.url: str = url
        self.size: PictureSize = PictureSize