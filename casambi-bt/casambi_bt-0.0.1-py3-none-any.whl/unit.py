from dataclasses import dataclass
from enum import Enum, unique
from typing import List


# Numbers are totally arbitrary so far.
@unique
class UnitControlType(Enum):
    DIMMER = 0
    WHITE = 1
    RGB = 2


@dataclass
class UnitControl:
    type: UnitControlType
    offset: int
    length: int
    default: bytes
    readonly: bool


@dataclass
class UnitType:
    id: int
    model: str
    mode: str
    stateLength: int
    controls: List[UnitControl]


@dataclass
class Unit:
    _typeId: int
    deviceId: int
    uuid: str
    address: str
    name: str
    state: bytes

    unitType: UnitType


@dataclass
class Scene:
    sceneId: int
    name: str


@dataclass
class Group:
    groudId: int
    name: str
