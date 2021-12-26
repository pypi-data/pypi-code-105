# Hugo - UserBot
# Copyright (C) 2021 TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamHugoX/pyHugo/blob/main/LICENSE>.

import os
import time
from logging import INFO, WARNING, FileHandler, StreamHandler, basicConfig, getLogger

from telethon import __version__

from .. import *
from ..version import __version__ as __pyHugo__
from ..version import hugo_version

if os.path.exists("hugo.log"):
    os.remove("hugo.log")

LOGS = getLogger("pyHgLogs")
TeleLogger = getLogger("Telethon")
TeleLogger.setLevel(WARNING)

basicConfig(
    format="%(asctime)s || %(name)s [%(levelname)s] : %(message)s",
    level=INFO,
    datefmt="%m/%d/%Y, %H:%M:%S",
    handlers=[FileHandler("hugo.log"), StreamHandler()],
)

LOGS.info(
    """
                -----------------------------------
                        Starting Deployment
                -----------------------------------
"""
)


LOGS.info(f"py-Hugo Version - {__pyHugo__}")
LOGS.info(f"Telethon Version - {__version__}")
LOGS.info(f"Hugo Version - {hugo_version}")
