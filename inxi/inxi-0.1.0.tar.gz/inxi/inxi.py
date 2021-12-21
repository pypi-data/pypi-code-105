import logging
import platform
from datetime import datetime
from typing import Optional

import psutil
import typer
from cpuinfo import get_cpu_info
from rich.console import Console
from rich.highlighter import NullHighlighter
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

console = Console(highlighter=NullHighlighter())
log = logging.getLogger("rich")


def cpu(verbose: bool = False):
    if verbose:
        logging.info("Getting CPU...")
    return get_cpu_info()["brand_raw"]


def kernel(verbose: bool = False):
    if verbose:
        logging.info("Getting kernel...")
    return platform.release()


def up(verbose: bool = False):
    if verbose:
        logging.info("Getting uptine...")
    boot_time = datetime.utcfromtimestamp(psutil.boot_time())
    difference = datetime.utcnow() - boot_time
    hours = int(difference.seconds / 60 / 60)
    minutes = int(difference.seconds / 60 / 60 / 60)
    return f"{difference.days}d {hours}h {minutes}m"


def main(verbose: Optional[bool] = False):
    console.print(
        f"[steel_blue bold]CPU:[/steel_blue bold] {cpu(verbose)} "
        f"[steel_blue bold]Kernel:[/steel_blue bold] {kernel(verbose)} "
        f"[steel_blue bold]Up:[/steel_blue bold] {up(verbose)} "
    )


if __name__ == "__main__":
    typer.run(main)
