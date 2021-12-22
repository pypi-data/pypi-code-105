from cenzopapa.resources import ImageResource

__version__ = "1.1.0"


class Cenzopapa:

    def __init__(self, api_url=None):
        self.api_url = api_url
        if not api_url:
            self.api_url = "https://api.jebzpapy.tk"

        self.image = ImageResource(api_url=self.api_url)
