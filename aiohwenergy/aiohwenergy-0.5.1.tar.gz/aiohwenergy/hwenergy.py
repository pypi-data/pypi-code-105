"""Representation of a HomeWizard Energy device."""
from __future__ import annotations

import logging
from types import TracebackType
from typing import Optional, Type

import aiohttp

from .data import Data
from .device import Device
from .errors import DisabledError, RequestError, UnsupportedError
from .state import State

_LOGGER = logging.getLogger(__name__)

SUPPORTED_API_VERSION = "v1"
SUPPORTED_DEVICES = ["HWE-P1", "SDM230-wifi", "SDM630-wifi", "HWE-SKT"]


class HomeWizardEnergy:
    """Communicate with a HomeWizard Energy device."""

    _clientsession: aiohttp.TCPConnector | None

    def __init__(self, host: str):
        """Create a HomeWizard Energy object."""
        _LOGGER.debug("__init__ HomeWizardEnergy")
        self._host = host
        self._clientsession = None
        self._device = None
        self._data = None
        self._state = None

    async def __aenter__(self) -> "HomeWizardEnergy":
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> Optional[bool]:
        """Exit context manager."""
        if self._clientsession is not None:
            await self.close()
        if exc_val:
            raise exc_val
        return exc_type

    @property
    def host(self) -> str:
        """Return the hostname of the device."""
        return self._host

    @property
    def device(self) -> Device | None:
        """Return the device object."""
        return self._device

    @property
    def data(self) -> Device | None:
        """Return the data object."""
        return self._data

    @property
    def state(self) -> State | None:
        """Return the state object."""
        return self._state

    async def initialize(self):
        """Initialize new Device object and validate connection."""

        self._device = Device(self.request)
        if not await self.device.update():
            _LOGGER.error("Failed to initalize API")
            return

        # Validate 'device'
        if self.device.api_version != SUPPORTED_API_VERSION:
            raise UnsupportedError(
                f"Unsupported API version, expected version '{SUPPORTED_API_VERSION}'"
            )

        if self.device.product_type not in SUPPORTED_DEVICES:
            raise UnsupportedError(f"Unsupported device '{self.device.product_type}'")

        # Get /data
        self._data = Data(self.request)
        status = await self.data.update()
        if not status:
            _LOGGER.error("Failed to get 'data'")

        # For HWE-SKT: Get /State
        if self.device.product_type == "HWE-SKT":
            self._state = State(self.request)
            status = await self.state.update()
            if not status:
                _LOGGER.error("Failed to get 'state' data")

    async def update(self) -> bool:
        """Fetch complete state for available endpoints."""
        _LOGGER.debug("hwenergy update")

        if self.device is not None:
            status = await self.device.update()
            if not status:
                return False

        if self.data is not None:
            status = await self.data.update()
            if not status:
                return False

        if self.state is not None:
            status = await self.state.update()
            if not status:
                return False

        return True

    async def close(self):
        """Close client session."""
        _LOGGER.debug("Closing clientsession")
        await self._clientsession.close()

    async def request(self, method: str, path: str, data: object = None) -> object | None:
        """Make a request to the API."""
        if self._clientsession is None:

            connector = aiohttp.TCPConnector(
                enable_cleanup_closed=True,
                limit_per_host=1,
            )
            self._clientsession = aiohttp.ClientSession(connector=connector)

        url = f"http://{self.host}/{path}"
        headers = {"Content-Type": "application/json"}

        _LOGGER.debug("%s, %s, %s", method, url, data)

        async with self._clientsession.request(
            method,
            url,
            json=data,
            headers=headers,
        ) as resp:
            _LOGGER.debug("%s, %s", resp.status, await resp.text("utf-8"))

            if resp.status == 403:
                # Known case: API disabled
                raise DisabledError(
                    "API disabled. API must be enabled in HomeWizard Energy app"
                )
            if resp.status != 200:
                # Something else went wrong
                raise RequestError(f"API request error ({resp.status})")

            data = None
            if resp.content_type != "application/json":
                raise RequestError("Unexpected content type")

            return await resp.json()
