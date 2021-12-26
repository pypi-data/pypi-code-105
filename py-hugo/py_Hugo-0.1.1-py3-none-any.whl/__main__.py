# Hugo - UserBot
# Copyright (C) 2021 TeamHugoX
#
# This file is a part of < https://github.com/TeamHugoX/Hugo/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamHugoX/pyHugo/blob/main/LICENSE>.

import os
import sys
import time

from . import *
from .functions.helper import time_formatter, updater
from .startup.funcs import autopilot, customize, plug, ready, startup_stuff
from .startup.loader import load_other_plugins

# Option to Auto Update On Restarts..
if udB.get("UPDATE_ON_RESTART") and os.path.exists(".git") and updater():
    os.system("git pull -f -q && pip3 install --no-cache-dir -U -q -r requirements.txt")
    os.execl(sys.executable, "python3", "-m", "pyHugo")

startup_stuff()


hugo_bot.me.phone = None
hugo_bot.first_name = hugo_bot.me.first_name

if not hugo_bot.me.bot:
    udB.set("OWNER_ID", hugo_bot.uid)


LOGS.info("Initialising...")


hugo_bot.run_in_loop(autopilot())

pmbot = udB.get("PMBOT")
manager = udB.get("MANAGER")
addons = udB.get("ADDONS") or Var.ADDONS
vcbot = udB.get("VCBOT") or Var.VCBOT

# Railway dont allow Music Bots
if HOSTED_ON == "railway" and not vcbot:
    vcbot = "False"

load_other_plugins(addons=addons, pmbot=pmbot, manager=manager, vcbot=vcbot)

suc_msg = """
            ----------------------------------------------------------------------
                Hugo has been deployed! Visit @HugoProject for updates!!
            ----------------------------------------------------------------------
"""

# for channel plugins
plugin_channels = udB.get("PLUGIN_CHANNEL")

# Customize Hugo Assistant...
hugo_bot.run_in_loop(customize())

# Load Addons from Plugin Channels.
if plugin_channels:
    hugo_bot.run_in_loop(plug(plugin_channels))

# Send/Ignore Deploy Message..
if not udB.get("LOG_OFF"):
    hugo_bot.run_in_loop(ready())


if __name__ == "__main__":
    LOGS.info(f"Took {time_formatter((time.time() - start_time)*1000)} to start •HUGO•")
    LOGS.info(suc_msg)
    hugo_bot.run()
