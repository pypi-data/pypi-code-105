import asyncio
from typing import Awaitable, List

from bleak import BleakScanner
from bleak.exc import BleakDBusError

from .errors import BluetoothError, BluetoothNotReadyError
from ._constants import CASA_UUID


async def discover() -> Awaitable[List[str]]:
    try:
        devices = await BleakScanner.discover()
    except BleakDBusError as e:
        if e.dbus_error == "org.bluez.Error.NotReady":
            raise BluetoothNotReadyError(e.dbus_error, e.dbus_error_details)
        else:
            raise BluetoothError(e.dbus_error, e.dbus_error_details)

    discovered = []
    for d in devices:
        if "manufacturer_data" in d.metadata and 963 in d.metadata["manufacturer_data"]:
            if CASA_UUID in d.metadata["uuids"]:
                discovered.append(d.address)

    return discovered
