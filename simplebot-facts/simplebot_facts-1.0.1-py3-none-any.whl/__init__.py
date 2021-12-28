"""Plugin's commands definitions"""

import bs4
import requests
import simplebot
from simplebot.bot import Replies

HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0)"
    " Gecko/20100101 Firefox/60.0"
}


@simplebot.command
def fact(replies: Replies) -> None:
    """Get a random fact from https://dailyfacts.org"""
    replies.add(text=_get_fact())


@simplebot.command
def factOfTheDay(replies: Replies) -> None:
    """Get the fact of the day from https://dailyfacts.org"""
    replies.add(text=_get_fact(""))


@simplebot.command
def factGeneral(replies: Replies) -> None:
    """Get a random fact from the "general" category."""
    replies.add(text=_get_fact("general"))


@simplebot.command
def factScience(replies: Replies) -> None:
    """Get a random fact from the "science" category."""
    replies.add(text=_get_fact("science"))


@simplebot.command
def factLifeHacks(replies: Replies) -> None:
    """Get a random fact from the "life-hacks" category."""
    replies.add(text=_get_fact("life-hacks"))


@simplebot.command
def factSports(replies: Replies) -> None:
    """Get a random fact from the "sports" category."""
    replies.add(text=_get_fact("sports"))


@simplebot.command
def factPsychology(replies: Replies) -> None:
    """Get a random fact from the "psychology" category."""
    replies.add(text=_get_fact("psychology"))


@simplebot.command
def factBody(replies: Replies) -> None:
    """Get a random fact from the "human-body" category."""
    replies.add(text=_get_fact("human-body"))


@simplebot.command
def factHistory(replies: Replies) -> None:
    """Get a random fact from the "history" category."""
    replies.add(text=_get_fact("history"))


@simplebot.command
def factTrivia(replies: Replies) -> None:
    """Get a random fact from the "trivia" category."""
    replies.add(text=_get_fact("trivia"))


@simplebot.command
def factSpooky(replies: Replies) -> None:
    """Get a random fact from the "spooky" category."""
    replies.add(text=_get_fact("spooky"))


@simplebot.command
def factFood(replies: Replies) -> None:
    """Get a random fact from the "food" category."""
    replies.add(text=_get_fact("food"))


@simplebot.command
def factTech(replies: Replies) -> None:
    """Get a random fact from the "technology" category."""
    replies.add(text=_get_fact("technology"))


@simplebot.command
def factNature(replies: Replies) -> None:
    """Get a random fact from the "nature" category."""
    replies.add(text=_get_fact("nature"))


@simplebot.command
def factAnimals(replies: Replies) -> None:
    """Get a random fact from the "animals" category."""
    replies.add(text=_get_fact("animals"))


@simplebot.command
def factCelebrities(replies: Replies) -> None:
    """Get a random fact from the "celebrities" category."""
    replies.add(text=_get_fact("celebrities"))


@simplebot.command
def factMovies(replies: Replies) -> None:
    """Get a random fact from the "movies" category."""
    replies.add(text=_get_fact("movies"))


@simplebot.command
def factUniverse(replies: Replies) -> None:
    """Get a random fact from the "universe" category."""
    replies.add(text=_get_fact("universe"))


@simplebot.command
def factWorld(replies: Replies) -> None:
    """Get a random fact from the "world" category."""
    replies.add(text=_get_fact("world"))


@simplebot.command
def factKids(replies: Replies) -> None:
    """Get a random fact from the "kids" category."""
    replies.add(text=_get_fact("kids"))


@simplebot.command
def factBusiness(replies: Replies) -> None:
    """Get a random fact from the "business" category."""
    replies.add(text=_get_fact("business"))


@simplebot.command
def factUS(replies: Replies) -> None:
    """Get a random fact from the "united-states" category."""
    replies.add(text=_get_fact("united-states"))


@simplebot.command
def factLanguage(replies: Replies) -> None:
    """Get a random fact from the "language" category."""
    replies.add(text=_get_fact("language"))


@simplebot.command
def factInternet(replies: Replies) -> None:
    """Get a random fact from the "internet" category."""
    replies.add(text=_get_fact("internet"))


def _get_fact(category: str = None) -> str:
    if category is None:
        with requests.get("https://dailyfacts.org/", headers=HEADERS) as resp:
            resp.raise_for_status()
            soup = bs4.BeautifulSoup(resp.text, "html.parser")
        url = soup.find("a", class_="nav-link", text="Random Fact")["href"]
    else:
        url = "https://dailyfacts.org/" + category

    with requests.get(url, headers=HEADERS) as resp:
        resp.raise_for_status()
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
    _fact = soup.find(class_="fact-content").text.strip()
    if not category:
        category = soup.find(class_="fact-categories").a.text.strip().replace(" ", "-")
    assert category
    return f"{_fact}\n\n#{''.join(map(str.capitalize, category.split('-')))} #Fact"
