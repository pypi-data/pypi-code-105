"""The ion package's catch-all module.

You should only add code to this module when you are unable to find ANY other
module to add it to.
"""

from __future__ import annotations

import logging
from subprocess import PIPE, Popen
import sys
import termios
from textwrap import wrap
import tty
from typing import Iterator


logger = logging.getLogger(__name__)


def getch(prompt: str = None) -> str:
    """Reads a single character from stdin.

    Args:
        prompt: prompt that is presented to user.

    Returns:
        The single character that was read.
    """
    if prompt:
        sys.stdout.write(prompt)

    sys.stdout.flush()

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def ewrap(
    multiline_msg: str, width: int = 80, indent: int = 0
) -> Iterator[str]:
    """A better version of textwrap.wrap()."""
    for msg in multiline_msg.split("\n"):
        if not msg:
            yield ""
            continue

        msg = (" " * indent) + msg

        i = 0
        while i < len(msg) and msg[i] == " ":
            i += 1

        spaces = " " * i
        for m in wrap(
            msg, width, subsequent_indent=spaces, drop_whitespace=True
        ):
            yield m


def efill(multiline_msg: str, width: int = 80, indent: int = 0) -> str:
    """A better version of textwrap.fill()."""
    return "\n".join(ewrap(multiline_msg, width, indent))


def confirm(prompt: str) -> bool:
    """Prompt user for 'y' or 'n' answer.

    Returns:
        True iff the user responds to the @prompt with 'y'.
    """
    prompt += " (y/n): "
    y_or_n = input(prompt)
    return y_or_n == "y"


def box(title: str) -> str:
    """Wraps @title in a pretty ASCII box."""
    middle = f"|          {title}          |"
    top = bottom = "+" + ("-" * (len(middle) - 2)) + "+"
    return f"{top}\n{middle}\n{bottom}"


def copy_to_clipboard(clip: str) -> None:
    """Copys a clip to the system clipboard.

    Args:
        clip: The clip that gets copied into the clipboard.
    """
    if _command_exists("xclip"):
        tool = "xclip"
        cmd_list = ["xclip", "-sel", "clip"]
    elif _command_exists("pbcopy"):
        tool = "pbcopy"
        cmd_list = ["pbcopy"]
    else:
        logger.warning("Neither xclip nor pbcopy are installed.")
        return

    popen = Popen(cmd_list, stdin=PIPE)
    popen.communicate(input=clip.encode())
    logger.info("Copied %s into clipboard using %s.", clip, tool)


def _command_exists(cmd: str) -> bool:
    """Returns True iff the shell command ``cmd`` exists."""
    popen = Popen("hash {}".format(cmd), shell=True, stdout=PIPE, stderr=PIPE)
    return popen.wait() == 0
