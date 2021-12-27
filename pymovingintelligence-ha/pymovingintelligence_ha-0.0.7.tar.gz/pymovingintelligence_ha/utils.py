"""Home Assistant Python 3 API wrapper for Moving Intelligence."""
import hashlib
import json
import logging
import secrets
import time
from typing import Optional

import requests
from requests.exceptions import HTTPError, RequestException, Timeout

_LOGGER = logging.getLogger("pymovingintelligence_ha")


class Utilities:
    """Utilities for Moving Intelligence."""

    def __init__(self, username, apikey):
        self._username = username
        self._apikey = apikey
        self._base_url = "https://api-app.movingintelligence.com"

    @staticmethod
    def clean_request_params(params: dict) -> dict:
        """Create clean parameters."""
        clean_params = {}
        for key, value in params.items():
            if value is not None:
                clean_params[key] = str(value)

        return clean_params

    def _create_headers(self, endpoint: str, params: dict) -> str:
        """Return signature."""
        params_string = ""
        nonce = secrets.token_hex(10)
        timestamp = int(time.time())

        if params:
            params_string = "&".join([f"{key}={val}" for key, val in params.items()])
            endpoint = f"{endpoint}?{params_string}"

        sha512str = (
            "sha512 "
            + hashlib.sha512(
                str(
                    endpoint + self._username + nonce + str(timestamp) + self._apikey
                ).encode("utf-8")
            ).hexdigest()
        )
        headers = {
            "X-Mi-User": self._username,
            "X-Mi-Nonce": nonce,
            "X-Mi-Timestamp": str(timestamp),
            "X-Signature": sha512str,
        }

        return headers

    def request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        body: dict = None,
    ) -> Optional[str]:
        """Makes a request to the movingintelligence API."""

        headers = self._create_headers(endpoint, params)
        url = f"{self._base_url}{endpoint}"

        _LOGGER.debug(
            "Making request to %s endpoint url: %s, headers: %s, params: %s, body: %s",
            endpoint,
            url,
            headers,
            params,
            body,
        )

        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                params=params,
                json=body,
                timeout=10,
            )

            log_msg = response.json()

            _LOGGER.debug("Request response: %s: %s", response.status_code, log_msg)

            response.raise_for_status()
            return response.json()
        except HTTPError:
            json_payload = {}
            try:
                json_payload = response.json()
            except json.decoder.JSONDecodeError:
                _LOGGER.debug("Invalid JSON payload received")

            if response.status_code == 500:
                raise InvalidAuthError("Invalid credentials")

            if response.status_code == 401:
                status = json_payload.get("status")
                message = json_payload.get("message")
                if status == "UNAUTHORIZED":
                    pass
                else:
                    _LOGGER.debug(
                        "Error occurred %s %s",
                        response.status_code,
                        message,
                    )
        except Timeout:
            _LOGGER.error(
                "Connection timed out occurred. Possible connectivity outage.",
            )
        except (RequestException, json.decoder.JSONDecodeError):
            _LOGGER.error("Error occurred while connecting.")

        return None


class InvalidAuthError(Exception):
    """Raised when API returns a code indicating invalid credentials."""


class InvalidPermissionsError(Exception):
    """Raised when API returns a code indicating not enough permissions."""
