import logging
from binascii import b2a_hex as b2a
from typing import Any, Awaitable, Callable, Dict, List, Union

from .errors import AuthenticationError, NetworkNotFoundError, ProtocolError
from ._client import CasambiClient, IncommingPacketType
from ._discover import discover
from ._network import Network, getNetworkIdFromUuid
from ._operation import OpCode, OperationsContext
from ._unit import Group, Scene, Unit


class Casambi:
    _casaClient: CasambiClient
    _casaNetwork: Network
    _opContext: OperationsContext

    _unitChangedCallbacks: List[Callable[[Unit], None]] = []

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)
        self._opContext = OperationsContext()

    # TODO: Support for multiple networks?
    async def connect(self, addr: str, password: str) -> Awaitable[None]:
        self._logger.info(f"Trying to connect to casambi network {addr}...")

        addrs = await discover()
        if addr not in addrs:
            raise NetworkNotFoundError

        self._casaClient = CasambiClient(addr, self._dataCallback)

        networkId = await getNetworkIdFromUuid(addr)
        self._casaNetwork = Network(networkId)
        if not self._casaNetwork.authenticated():
            loggedIn = await self._casaNetwork.logIn(password)
            if not loggedIn:
                raise AuthenticationError("Login failed")
        await self._casaNetwork.update()

        await self._casaClient.connect()
        try:
            await self._casaClient.exchangeKey()
            await self._casaClient.authenticate(self._casaNetwork.getKeyStore())
        except ProtocolError as e:
            await self._casaClient.disconnect()
            raise e

    async def setState(
        self, target: Union[Unit, Group, Scene, None], state: bytes
    ) -> Awaitable[None]:
        targetCode = 0
        if isinstance(target, Unit):
            assert target.deviceId <= 0xFF
            targetCode = (target.deviceId << 8) | 0x01
        elif isinstance(target, Group):
            assert target.groudId <= 0xFF
            targetCode = (target.groudId << 8) | 0x02
        elif isinstance(target, Scene):
            assert target.sceneId <= 0xFF
            targetCode = (target.sceneId << 8) | 0x04
        elif target is not None:
            raise TypeError(f"Unkown target type {type(target)}")

        self._logger.info(f"Setting state for {targetCode:x}...")

        opPkt = self._opContext.prepareOperation(OpCode.SetLevel, targetCode, state)

        await self._casaClient.send(opPkt)

    def _dataCallback(
        self, packetType: IncommingPacketType, data: Dict[str, Any]
    ) -> None:
        self._logger.info(f"Incomming data callback of type {packetType}")
        if packetType == IncommingPacketType.UnitState:
            self._logger.debug(
                f"Handling changed state {b2a(data['state'])} for unit {data['id']}"
            )

            found = False
            for u in self._casaNetwork.units:
                if u.deviceId == data["id"]:
                    found = True
                    u.state = data["state"]

                    # Notify listeners
                    for h in self._unitChangedCallbacks:
                        h(u)

            if not found:
                self._logger.error(
                    f"Changed state notification for unkown unit {data['id']}"
                )

        else:
            self._logger.warning(f"Handler for type {packetType} not implemented!")

    def registerUnitChangedHandler(self, handler: Callable[[Unit], None]) -> None:
        self._unitChangedCallbacks.append(handler)
        self._logger.info(f"Registerd unit changed handler {handler}")

    def unregisterUnitChangedHandler(self, handler: Callable[[Unit], None]) -> None:
        self._unitChangedCallbacks.remove(handler)
        self._logger.info(f"Removed unit changed handler {handler}")

    async def disconnect(self) -> Awaitable[None]:
        if self._casaClient:
            await self._casaClient.disconnect()
        if self._casaNetwork:
            await self._casaNetwork.disconnect()

    async def __aexit__(self) -> Awaitable[None]:
        await self.disconnect()
