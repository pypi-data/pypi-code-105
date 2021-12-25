###########################
####    v4yve corp.    ####
####  bomber by v4yve  ####
####   cli.py - файл   ####
###########################

# Библиотеки
import asyncio
import os
import sys

import click
import pkg_resources
import uvicorn
from loguru import logger

os.chdir(os.path.join(pkg_resources.get_distribution("v4yve").location, "v4yve"))

from v4yve.app.main import app
from v4yve.service import prepare_services
from v4yve.utils import open_url


@logger.catch
@click.command()
@click.option("--ip", default="127.0.0.1")
@click.option("--port", default=8080)
@click.option("--only-api", "only_api", is_flag=True, default=False)
def main(ip: str, port: int, only_api: bool = False):
    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)

    app.state.only_api = only_api

    prepare_services()

    if not only_api:
        open_url(f"http://{ip}:{port}/")

    uvicorn.run(app, host=ip, port=port, log_level="error")


main()
