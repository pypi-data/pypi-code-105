"""Hooks for the 'pass' tool.

See the tool's official documentation[1] for more information.

[1]: https://www.passwordstore.org
"""

import logging
from typing import Iterable, Optional

from eris import Err
import proctor

from .. import hookimpl


logger = logging.getLogger(__name__)


@hookimpl  # type: ignore[misc]
def get_secret(
    key: str, namespace: Iterable[str], user: Optional[str]
) -> Optional[str]:
    """Implements get_secret() hook using 'pass'."""
    if not proctor.command_exists("pass"):
        logger.debug(
            "The 'pass' command does not appear to exist on this machine."
        )
        return None

    if namespace:
        key = f"{'/'.join(namespace)}/{key}"

    cmd_list = []
    if user is not None:
        cmd_list.extend(["sudo", "-u", user])

    cmd_list.extend(["pass", "show", key])

    process_result = proctor.safe_popen(cmd_list)
    if isinstance(process_result, Err):
        error = process_result.err()
        logger.debug(
            "Unable to retrieve secret using 'pass': %r", error.to_json()
        )
        return None

    secret, _ = process_result.ok()
    return secret
