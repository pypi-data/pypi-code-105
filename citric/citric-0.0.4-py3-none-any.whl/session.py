"""Low level wrapper for connecting to the LSRC2."""
import logging
import random
from types import TracebackType
from typing import Any, Optional, Type, TypeVar

import requests

from citric.exceptions import (
    LimeSurveyError,
    LimeSurveyStatusError,
    LimeSurveyApiError,
)
from citric.method import Method

_T = TypeVar("_T", bound="Session")
logger = logging.getLogger(__name__)


class Session:
    """LimeSurvey RemoteControl 2 session.

    Args:
        url: LimeSurvey Remote Control endpoint.
        username: LimeSurvey user name.
        password: LimeSurvey password.
        requests_session: A `requests.Session`_ object.

    .. _requests.Session:
        https://docs.python-requests.org/en/latest/api/#requests.Session
    """

    _headers = {
        "content-type": "application/json",
        "user-agent": "citric-client",
    }

    __attrs__ = ["url", "key"]

    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        requests_session: requests.Session = requests.session(),
    ) -> None:
        """Create a LimeSurvey RPC session."""
        self.url = url
        self._session = requests_session
        self._session.headers.update(self._headers)

        self.__key: Optional[str] = self.get_session_key(username, password)

        if self.get_site_settings("RPCInterface") != "json":
            raise LimeSurveyError("JSON RPC interface is not enabled.")

        self.__closed = False

    @property
    def closed(self) -> bool:
        """Whether the RPC session is closed."""
        return self.__closed

    @property
    def key(self) -> Optional[str]:
        """RPC session key."""
        return self.__key

    def __getattr__(self, name: str) -> Method:
        """Magic method dispatcher."""
        return Method(self.rpc, name)

    def rpc(self, method: str, *params: Any) -> Any:
        """Execute RPC method on LimeSurvey, with optional token authentication.

        Any method, except for `get_session_key`.

        Args:
            method: Name of the method to call.
            params: Positional arguments of the RPC method.

        Returns:
            An RPC result.
        """
        if method == "get_session_key" or method.startswith("system."):
            result = self._invoke(self._session, self.url, method, *params)
        # Methods requiring authentication
        else:
            result = self._invoke(self._session, self.url, method, self.key, *params)

        return result

    @staticmethod
    def _invoke(session: requests.Session, url: str, method: str, *params: Any) -> Any:
        """Execute a LimeSurvey RPC with a JSON payload.

        Args:
            session (requests.Session): An HTTP session for communication with
                the LSRC2 API.
            url: URL of the LSRC2 API.
            method (str): Name of the method to call.
            params (Any): Positional arguments of the RPC method.

        Raises:
            LimeSurveyStatusError: The response key from the response payload has
                a non-null status.
            LimeSurveyApiError: The response payload has a non-null error key.
            LimeSurveyError: Request ID does not match the response ID.

        Returns:
            Any: An RPC result.
        """
        request_id = random.randint(1, 999_999)

        payload = {
            "method": method,
            "params": [*params],
            "id": request_id,
        }

        res = session.post(url, json=payload)
        res.raise_for_status()

        if res.text == "":
            raise LimeSurveyError("RPC interface not enabled")

        data = res.json()

        result = data["result"]
        error = data["error"]
        response_id = data["id"]
        logger.info("Invoked RPC method %s with ID %d", method, request_id)

        if isinstance(result, dict) and result.get("status") not in {"OK", None}:
            raise LimeSurveyStatusError(result["status"])

        if error is not None:
            raise LimeSurveyApiError(error)

        if response_id != request_id:
            raise LimeSurveyError(
                f"Response ID {response_id} does not match request ID {request_id}",
            )

        return result

    def close(self) -> None:
        """Close RPC session."""
        self.release_session_key()
        self._session.close()
        self.__key = None
        self.__closed = True

    def __enter__(self: _T) -> _T:
        """Context manager for RPC session.

        Returns:
            LimeSurvey RPC session.
        """
        return self

    def __exit__(
        self,
        type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Safely exit an RPC session.

        Args:
            type: Exception class.
            value: Exception instance.
            traceback: Error traceback.
        """
        self.close()
