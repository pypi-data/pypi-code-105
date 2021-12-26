# Hugo - UserBot
# Copyright (C) 2021 TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamHugoX/pyHugo/blob/main/LICENSE>.

import inspect
import re

from telethon import Button
from telethon.events import CallbackQuery, InlineQuery, NewMessage
from telethon.tl.types import InputWebDocument
from telethon.utils import get_display_name

from .. import LOGS, asst, hugo_bot
from . import append_or_update, owner_and_sudos

HUGO_PIC = "https://telegra.ph/file/221e561192f96302a09d2.jpg"
OWNER = get_display_name(hugo_bot.me)

MSG = f"""
**Hugo - UserBot**
┈───────────────┈
**Owner**: [{OWNER}](tg://user?id={hugo_bot.uid})
**Support**: @HugoProject
┈───────────────┈
"""

IN_BTTS = [
    [
        Button.url(
            "Repository",
            url="https://github.com/TeamHugoX/Hugo",
        ),
        Button.url("Support", url="https://t.me/HugoSupport"),
    ]
]


# decorator for assistant


def asst_cmd(pattern=None, load=None, **kwargs):
    """Decorator for assistant's command"""
    name = inspect.stack()[1].filename.split("/")[-1].replace(".py", "")

    def hg(func):
        if pattern:
            kwargs["pattern"] = re.compile("^/" + pattern)
        asst.add_event_handler(func, NewMessage(**kwargs))
        if load is not None:
            append_or_update(load, func, name, kwargs)

    return hg


def callback(data=None, owner=False, **kwargs):
    """Assistant's callback decorator"""

    def hgr(func):
        async def wrapper(event):
            if owner and not str(event.sender_id) in owner_and_sudos():
                return await event.answer(f"This is {OWNER}'s bot!!")
            try:
                await func(event)
            except Exception as er:
                LOGS.exception(er)

        asst.add_event_handler(wrapper, CallbackQuery(data=data, **kwargs))

    return hgr


def in_pattern(pattern=None, owner=False, **kwargs):
    """Assistant's inline decorator."""

    def don(func):
        async def wrapper(event):
            if owner and not str(event.sender_id) in owner_and_sudos():
                res = [
                    await event.builder.article(
                        title="Hugo Userbot",
                        url="https://t.me/HugoProject",
                        description="(c) HugoProject",
                        text=MSG,
                        thumb=InputWebDocument(HUGO_PIC, 0, "image/jpeg", []),
                        buttons=IN_BTTS,
                    )
                ]
                return await event.answer(
                    res,
                    switch_pm=f"🤖: Assistant of {OWNER}",
                    switch_pm_param="start",
                )
            try:
                await func(event)
            except Exception as er:
                LOGS.exception(er)

        asst.add_event_handler(wrapper, InlineQuery(pattern=pattern, **kwargs))

    return don
