"""Plugin's commands definition."""

import functools

import requests
import simplebot
from simplebot.bot import Replies

tv_emoji, cal_emoji, aster_emoji = "📺", "📆", "✳"
channels = {
    "cv": "Cubavisión",
    "cvi": "Cubavisión Internacional",
    "cvplus": "Cubavisión Plus",
    "tr": "Tele Rebelde",
    "edu": "Educativo",
    "edu2": "Educativo 2",
    "mv": "Multivisión",
    "clave": "Clave",
    "caribe": "Caribe",
    "chabana": "Canal Habana",
}
session = requests.Session()
session.headers.update(
    {
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
    }
)
session.request = functools.partial(session.request, timeout=15)  # type: ignore


@simplebot.command
def cartv(replies: Replies) -> None:
    """Muestra la cartelera de todos los canales de la TV cubana."""
    replies.add(text="\n\n".join(_get_channel(chan) for chan in channels))


@simplebot.command
def cartvcv(replies: Replies) -> None:
    """Muestra la cartelera del canal Cubavisión."""
    replies.add(text=_get_channel("cv"))


@simplebot.command
def cartvcvi(replies: Replies) -> None:
    """Muestra la cartelera del canal Cubavisión Internacional."""
    replies.add(text=_get_channel("cvi"))


@simplebot.command
def cartvcvp(replies: Replies) -> None:
    """Muestra la cartelera del canal Cubavisión Plus."""
    replies.add(text=_get_channel("cvplus"))


@simplebot.command
def cartvtr(replies: Replies) -> None:
    """Muestra la cartelera del canal Tele Rebelde."""
    replies.add(text=_get_channel("tr"))


@simplebot.command
def cartved(replies: Replies) -> None:
    """Muestra la cartelera del canal Educativo."""
    replies.add(text=_get_channel("edu"))


@simplebot.command
def cartved2(replies: Replies) -> None:
    """Muestra la cartelera del canal Educativo 2."""
    replies.add(text=_get_channel("edu2"))


@simplebot.command
def cartvmv(replies: Replies) -> None:
    """Muestra la cartelera del canal Multivisión."""
    replies.add(text=_get_channel("mv"))


@simplebot.command
def cartvcl(replies: Replies) -> None:
    """Muestra la cartelera del canal Clave."""
    replies.add(text=_get_channel("clave"))


@simplebot.command
def cartvca(replies: Replies) -> None:
    """Muestra la cartelera del canal Caribe."""
    replies.add(text=_get_channel("caribe"))


@simplebot.command
def cartvha(replies: Replies) -> None:
    """Muestra la cartelera del canal Habana."""
    replies.add(text=_get_channel("chabana"))


def _get_channel(chan) -> str:
    url = f"https://www.tvcubana.icrt.cu/cartv/{chan}/hoy.php"
    with session.get(url) as req:
        req.raise_for_status()
        programs = req.json()

    text = f"{tv_emoji} {channels[chan]}\n"
    date = None
    for prog in programs:
        date2, time = prog["eventInitialDateTime"].split("T")
        time = time[:-3]
        if date != date2:
            date = date2
            text += f"{cal_emoji} {date}\n"
        title = " ".join(prog["title"].split())
        desc = " ".join(prog["description"].split())
        trans = prog["transmission"].strip()
        text += (
            f"{aster_emoji} {time} {'/'.join(e for e in (title, desc, trans) if e)}\n"
        )

    if not programs:
        text += "Cartelera no disponible."

    return text
