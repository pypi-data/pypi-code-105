from wire_web.response import PlainTextResponse
from mimetypes import MimeTypes

import os


class StaticFiles:
    def __init__(self, path: str) -> None:
        self.path = path

    def provide(self, filepath: str):
        mime = MimeTypes()
        typ = mime.guess_type("." + filepath)
        with open("." + filepath, "rb") as f:
            content = f.read()
        return content, typ[0]
