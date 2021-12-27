import urllib
from typing import Any, Dict, List, Union

from ...utils.utils import dt
from ..base import Ch, Downloader, Manga, Search, soup


def chapter(url: str) -> Ch:
    """
    Return a Ch object from the given url.

    Args:
        url (str): url of the chapter

    Returns:
        Ch
    """
    ms = soup(url)
    ch = "ch"
    return Ch(
        url              = url,
        ch               = ch,
        vol              = "vol",
        title            = f"Chapter {ch}",
        views            = "views",
        uploaded_at      = dt("uploaded_at", "format"),
        scanlator_groups = ["scanlator_groups"],
        user             = "user",
        imgs             = ["imgs"],
    )

def manga(url: str, chs: int=0) -> Manga:
    """Returns a Manga object from the given url.

    Args:
        url (str): url of the manga

    Returns:
        Manga
    """

    ms = soup(url)

    def chap_dict():
        op = {}
        for i in []:
            cch = i["url"]
            if chs == 2:
                cch = chapter(cch)
            op[i["ch"]] = cch
        return op

    return Manga(
        url=url,
        covers="covers",
        title="title",
        alt_titles="alt_titles",
        author="author",
        status="status",
        demographics="demographics",
        content_rating="content_rating",
        genres="genres",
        updated_at=dt("updated_at", "format"),
        created_at=dt("created_at", "format"),
        views="views",
        description="description",
        links="links",
        chapters=chap_dict(),
    )

def dl_search(title: str, **kwargs: Dict[str, Any]):
    """Search for manga using the given Search object that contains the search
    parameters. Used for downloading when imported.

    Args:
        s (Search): The Search obhect that contains the search parameters

    Returns:
        Dict[str, str]: The search results
    """

    sr = {}
    ms = soup(f"https://example.com/?s={urllib.parse.quote_plus(title)}")
    for r in ms.select("search results"):
        sr[r["title"]] = r["href"]
    return sr

def search(s: Search) -> List[Manga]:
    return [manga(i) for i in dl_search(s).values()]

def cli_search(title: str, **kwargs: Dict[str, Any]):
    # format the arguments if necessary
    return dl_search(title, **kwargs)

def ch_fn(url: str) -> List[str]:
    """CHapter FuNction
    Returns a list of image urls from the given chapter url.

    Args:
        url (str): The url of the chapter to get the images' links from

    Returns:
        List[str]: List of image urls
    """
    return [i["src"] for i in soup(url).select("img")]


def chdls(url: str) -> List[Dict[Union[float, int, None], str]]:
    """CHapter Dictionary LiSt
    Returns a list of dictionaries—with the chapter number and url as the key
    and value respectively—from the given url.

    Args:
        url (str): The url of the manga to get the chapters from

    Returns:
        List[Dict[Union[float, int, None], str]]: The List of dictionaries
            containing the chapter number and url
    """
    op = []
    ms = soup(url)
    for c in ["chapters"]:
        op.append({c["ch"]: c["href"]})
    return op

def dl(url: str, **kwargs: Dict[str, Any]):
    """Used for downloading when using the project as a module.

    Args:
        url (str): URL of the manga to download.
    """
    ms = soup(url)
    Downloader(ch_fn, **kwargs).dl_chdls(chdls(url), ms.select_one("title").text)

def cli_dl(title: str, **kwargs: Dict[str, Any]):
    """Used for downloading when using cli.

    Args:
        title (str): Title of the manga to download.
    """
    Downloader(ch_fn, **kwargs).cli(cli_search, chdls, title)
