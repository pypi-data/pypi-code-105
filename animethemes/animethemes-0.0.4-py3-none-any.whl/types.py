

class Anime:
    def __init__(self,
                 _id: int =None,
                 name: str = None,
                 slug: str = None,
                 year: int = None,
                 season: str = None,
                 synopsis: str = None,
                 created_at: str = None,
                 updated_at: str = None,
                 deleted_at: str = None,
                 animethemes: list = None
                 ):
        self.id = _id
        self.name = name
        self.slug = slug
        self.year = year
        self.season = season
        self.synopsis = synopsis
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.animethemes = animethemes


class AnimeTheme:
    def __init__(self,

                 ):
        pass

_d = ""

for i in _d:
    print(i)

