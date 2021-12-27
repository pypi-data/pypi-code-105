import urllib
from time import strftime, strptime
from typing import Any, Dict, List

from ...utils.globals import log
from ...utils.utils import dt
from ..Base import Ch, Downloader, Manga, Search, soup


def manga(url: str) -> Manga:
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
            op[i["ch"]] = Ch(
                url         = i["url"],
                ch          = i["ch"],
                vol         = i["vol"],
                title       = i["title"],
                user        = i["user"],
                uploaded_at = strftime("%Y-%m-%dT%H:%M:%S", strptime(i["uploaded_at"], "format")),
            )
        return op

    return Manga(
        url             = url,
        covers          = "covers",
        title           = "title",
        alt_titles      = "alt_titles",
        author          = "author",
        status          = "status",
        demographics    = "demographics",
        content_rating  = "content_rating",
        genres          = "genres",
        updated_at      = dt("updated_at", "format"),
        created_at      = dt("created_at", "format"),
        views           = "views",
        description     = "description",
        links           = "links",
        chapters        = chap_dict(),
    )

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
        uploaded_at      = "uploaded_at",
        scanlator_groups = ["scanlator_groups"],
        user             = "user",
        imgs             = ["imgs"],
    )

def dl_search(title: str, **kwargs: Dict[str, Any]):
    """Used for downloading when imported.

    Args:
        s (Search): [description]

    Returns:
        Dict[str, str]: [description]
    """

    sr = {}
    ms = soup(f"https://flamescans.org/?s={urllib.parse.quote_plus(title)}")
    pages = ms.select("a.page-numbers")
    if pages:
        log.debug("Multiple pages found. Starting to paginate.", "paginator")
        for p in range(int(pages[-2].text)):
            log.debug(f"Paginating page {p+1}.", "paginator")
            for r in soup(f"https://flamescans.org/page/{p+1}/?s={urllib.parse.quote_plus(title)}").select(".listupd .bs .bsx a"):
                if not r.select_one(".limit .novelabel"):
                    sr[r["title"]] = r["href"]
    else:
        log.debug("Only one page found.", "search")
        for r in ms.select(".listupd .bs .bsx a"):
            sr[r["title"]] = r["href"]
    return sr

def search(s: Search) -> List[Manga]:
    """Can be used for searching manga when using this project as a module.

    Args:
        s (Search): Search dataclass, search parameters for searching.

    Returns:
        List[Manga]: Search results.
    """
    return [manga(i) for i in dl_search(s).values()]

def cli_search(title: str, **kwargs: Dict[str, Any]):
    """Format click arguments and options to their respective types,
    then pass that to `dl_search` for it to return the search results.

    Args:
        title (str): Title of the manga to search for.

    Returns:
        Dict[str, str]: Search results
    """

    log.info("Ignoring all keword arguments.", "cli_search")
    return dl_search(title, **kwargs)

def dl(url: str, **kwargs: Dict[str, Any]):
    ms = soup(url)
    def ch_fn(url: str):
        return [i["src"] for i in soup(url).select("#readerarea p img")]
    chdls = []
    for c in ms.select("div.eplister ul li"):
        chdls.append({c["data-num"]: c.select_one("a")["href"]})
    Downloader(ch_fn, **kwargs).dl(ms.select_one("h1.entry-title").text, chdls)

def cli_dl(title: str, **kwargs: Dict[str, Any]):
    """Used for downloading when using cli.

    Args:
        title (str): Title of the manga to download.
    """
    sr = cli_search(title)
    def ch_fn(url: str):
        return [i["src"] for i in soup(url).select("#readerarea p img")]
    def chs_fn(choice: str):
        op = []
        url = sr[choice]
        for c in soup(url).select("div.eplister ul li"):
            op.append({c["data-num"]: c.select_one("a")["href"]})
        return op
    Downloader(ch_fn, **kwargs).cli(sr, chs_fn)
