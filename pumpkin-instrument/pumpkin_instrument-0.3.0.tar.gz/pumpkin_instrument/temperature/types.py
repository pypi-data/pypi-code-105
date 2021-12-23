# coding: utf-8
# ##############################################################################
#  (C) Copyright 2021 Pumpkin, Inc. All Rights Reserved.                       #
#                                                                              #
#  This file may be distributed under the terms of the License                 #
#  Agreement provided with this software.                                      #
#                                                                              #
#  THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,                   #
#  INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND                       #
#  FITNESS FOR A PARTICULAR PURPOSE.                                           #
# ##############################################################################
"""
All types and protocols needed to interface with temperature sensors
"""
from abc import abstractmethod
from enum import Enum
from typing import NamedTuple, Optional, List

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol


class TemperatureUnit(Enum):
    """
    Which type of temperature unit to use
    """
    Celcius = 0
    Farenheit = 1
    Kelvin = 2
    Voltage = 3


class ThermocoupleType(Enum):
    B = 0
    E = 1
    J = 2
    K = 3
    R = 4
    S = 5
    T = 6


class TemperatureSensor(Protocol):
    """
    The base protocol that implements a temperature sensor with one or more channels.
    """
    def set_units(self, ch: int, units: TemperatureUnit):
        """Sets the temperature units to use for the channel given"""
        raise NotImplementedError()

    def measure_temp(self, ch: int) -> float:
        """Measures the given temperature for the channel"""
        raise NotImplementedError()

    def set_alarm(self, ch: int, low_temp: Optional[float] = None, high_temp: Optional[float] = None):
        """
        Sets the alarm to trigger when the temperature is out of bounds.
        If one parameter is `None`, then the temperature alarm only has an Upper/lower bound depending on the alarm set.
        If both parameters are `None`, then the alarm is disabled.
        """
        raise NotImplementedError()

    def get_alarms(self) -> List[int]:
        """
        Gets all of the alarm bits and returns them as a list of whether the bit is tripped or not.
        Each bit in the list returned corresponds to an alarm on a specific channel.
        """
        raise NotImplementedError()

    def set_thermocouple_type(self, ch: int, thermocouple_type: ThermocoupleType):
        """Sets the type of thermocouple used on the channel, see the ThermocoupleType enum for possible choices."""
        raise NotImplementedError()
