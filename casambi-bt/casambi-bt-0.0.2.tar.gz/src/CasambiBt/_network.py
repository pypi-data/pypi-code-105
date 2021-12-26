import asyncio
import logging
import pickle
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Awaitable, Dict, List, Optional

import httpx
from httpx import AsyncClient

from ._constants import BASE_PATH, DEVICE_NAME
from .errors import AuthenticationError
from ._keystore import KeyStore
from ._unit import Group, Scene, Unit, UnitControl, UnitControlType, UnitType


@dataclass()
class _NetworkSession:
    session: str
    network: str
    manager: bool
    keyID: int
    role: 3
    expires: datetime

    def expired(self) -> bool:
        return datetime.utcnow() > self.expires


class Network:
    _session: _NetworkSession = None
    _unitTypes: Dict[int, UnitType] = {}

    units: List[Unit] = []
    groups: List[Group] = []
    scenes: List[Scene] = []

    def __init__(self, id: str) -> None:
        self._logger = logging.getLogger(__name__)
        self._keystore = KeyStore(id)
        self._id = id
        basePath = Path(BASE_PATH / id)

        if not basePath.exists():
            basePath.mkdir(parents=True)

        self._sessionPath = basePath / "session.pck"
        if self._sessionPath.exists():
            self._loadSession()

        self._typeCachePath = basePath / "types.pck"
        if self._typeCachePath.exists():
            self._loadTypeCache()

    def _loadSession(self) -> None:
        self._logger.info("Loading session...")
        self._session = pickle.load(self._sessionPath.open("rb"))

    def _saveSesion(self) -> None:
        self._logger.info("Saving session...")
        pickle.dump(self._session, self._sessionPath.open("wb"))

    def _loadTypeCache(self) -> None:
        self._logger.info("Loading unit type cache...")
        self._unitTypes = pickle.load(self._typeCachePath.open("rb"))

    def _saveTypeCache(self) -> None:
        self._logger.info("Saving type cache...")
        pickle.dump(self._unitTypes, self._typeCachePath.open("wb"))

    def authenticated(self) -> bool:
        if not self._session:
            return False
        return not self._session.expired()

    def getKeyStore(self) -> KeyStore:
        return self._keystore

    async def logIn(self, password: str) -> Awaitable[bool]:
        self._logger.info(f"Logging in to network...")
        getSessionUrl = f"https://api.casambi.com/network/{self._id}/session"
        async with AsyncClient() as request:
            res = await request.post(
                getSessionUrl, json={"password": password, "deviceName": DEVICE_NAME}
            )
            if res.status_code == httpx.codes.OK:
                sessionJson = res.json()
                sessionJson["expires"] = datetime.utcfromtimestamp(
                    sessionJson["expires"] / 1000
                )
                self._session = _NetworkSession(**sessionJson)
                self._logger.info("Login sucessful.")
                self._saveSesion()
                return True
            else:
                self._logger.error(f"Login failed: {res.status_code}\n{res.text}")
                return False

    async def update(self) -> Awaitable[bool]:
        self._logger.info(f"Updating network...")
        if not self.authenticated():
            raise AuthenticationError("Not authenticated!")

        # TODO: Save and send revision to receive actual updates?

        getNetworkUrl = f"https://api.casambi.com/network/{self._id}/"
        async with AsyncClient() as request:
            request.headers["X-Casambi-Session"] = self._session.session
            res = await request.put(
                getNetworkUrl, json={"formatVersion": 1, "deviceName": DEVICE_NAME}
            )

        if res.status_code != httpx.codes.OK:
            self._logger.error(f"Update failed: {res.status_code}\n{res.text}")
            return False

        self._logger.debug(f"Network: {res.text}")

        resJson = res.json()

        # Parse keys
        keys = resJson["network"]["keyStore"]["keys"]
        for k in keys:
            self._keystore.addKey(k)

        # Parse units
        units = resJson["network"]["units"]
        for u in units:
            uType = await self._fetchUnitInfo(u["type"])
            uObj = Unit(
                u["type"],
                u["deviceID"],
                u["uuid"],
                u["address"],
                u["name"],
                None,
                uType,
            )
            self.units.append(uObj)

        # Parse cells
        cells = resJson["network"]["grid"]["cells"]
        for c in cells:
            # Only one type at top level is currently supported
            if c["type"] != 2:
                continue
            gObj = Group(c["groupID"], c["name"])
            self.groups.append(gObj)

        # Parse scenes
        scenes = resJson["network"]["scenes"]
        for s in scenes:
            sObj = Scene(s["sceneID"], s["name"])
            self.scenes.append(sObj)

        # TODO: Parse more stuff

        self._saveTypeCache()

        self._logger.info("Network updated.")
        return True

    async def _fetchUnitInfo(self, id: int) -> Awaitable[UnitType]:
        self._logger.info(f"Fetching unit type for id {id}...")
        cachedType = self._unitTypes.get(id)
        if cachedType:
            self._logger.info("Using cached type.")
            return cachedType

        getUnitInfoUrl = f"https://api.casambi.com/fixture/{id}"
        async with AsyncClient() as request:
            res = await request.get(getUnitInfoUrl)

        if res.status_code != httpx.codes.OK:
            self._logger.error(f"Getting unit info returned {res.status_code}")

        unitTypeJson = res.json()
        controls = []
        for controlJson in unitTypeJson["controls"]:
            typeStr = controlJson["type"].upper()
            type = UnitControlType[typeStr]
            controlObj = UnitControl(
                type,
                controlJson["offset"],
                controlJson["length"],
                controlJson["default"],
                controlJson["readonly"],
            )
            controls.append(controlObj)

        unitTypeObj = UnitType(
            unitTypeJson["id"],
            unitTypeJson["model"],
            unitTypeJson["mode"],
            unitTypeJson["stateLength"],
            controls,
        )
        self._unitTypes[unitTypeObj.id] = unitTypeObj
        self._logger.info("Sucessfully fetched unit type.")
        return unitTypeObj

    async def disconnect(self) -> Awaitable[None]:
        pass  # TODO: Reuse network client


async def getNetworkIdFromUuid(mac: str) -> Awaitable[Optional[str]]:
    _logger = logging.getLogger(__name__)
    _logger.info(f"Getting network id...")
    getNetworkIdUrl = f"https://api.casambi.com/network/uuid/{mac.replace(':', '')}"
    async with AsyncClient() as request:
        res = await request.get(getNetworkIdUrl)

    if res.status_code != httpx.codes.OK:
        _logger.error(f"Getting network id returned {res.status_code}")

    id = res.json()["id"]
    _logger.info(f"Got network id {id}.")
    return id
