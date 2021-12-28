import cloudscraper
from bs4 import BeautifulSoup

# url = "https://staging.animethemes.moe/api/anime/" + "gamers"
# url = "https://staging.animethemes.moe/api/search"
# data = {
#     "q": "Gamer"
    # "include[anime]": "resources"
# }
# c = cloudscraper.create_scraper()
# r = c.get(url, params=data).json()
# r = c.get(url).json()
# print(r)
# for i in r["search"]["anime"]:
#     print(i)


class AnimeThemes:
    def __init__(self):
        self.__base = "https://staging.animethemes.moe/api/"
        self.__session = cloudscraper.create_scraper()
        self.__params = {}

    def __session_requests(self, url, method="GET"):
        return self.__session.request(method, url, params=self.__params)

    def __set_params(self, params: dict = None):
        return self.__params.update(params)

    def search(self, query):
        self.__params.update(
            {
                "q": query,
                "include[anime]": "animethemes.animethemeentries.videos"
                # "include[anime]": "resources"
            }
        )
        return self.__session_requests(
            self.__base + "search"
        ).json()

    def search_anime(self, query: str = None, anime_id: int = None):
        _include = "animethemes.animethemeentries.videos,images"
        if query:
            self.__set_params(
                {
                    "q": query,
                    "include": _include
                }
            )
        elif anime_id:
            self.__set_params(
                {
                    "filter[id]": anime_id,
                    "include": _include
                }
            )
        else:
            pass
        return self.__session_requests(
            self.__base + "anime"
        ).json()

    def video(self, basename):
        return self.__session_requests(
            self.__base + "video/" + basename
        ).json()

    def anime(self, slug: str = None):
        self.__set_params(
            {
                "include": "animethemes.animethemeentries.videos,images"
            }
        )
        _da = self.__session_requests(
            self.__base + "anime/" + slug
        )
        if _da.status_code == 200:
            return _da.json()
        else:
            return _da.content

    def animethemes(self, theme_id: int):
        self.__set_params(
            {
                "include": "animethemeentries.videos"
            }
        )
        return self.__session_requests(
            self.__base + "animetheme/" + str(theme_id)
        ).json()
