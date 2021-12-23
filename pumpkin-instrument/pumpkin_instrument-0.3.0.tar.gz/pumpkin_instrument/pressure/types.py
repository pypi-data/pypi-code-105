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
All types and protocols needed to interface with pressure gauges.
"""
from abc import abstractmethod
from enum import Enum
from typing import NamedTuple, Optional
try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol


class PressureUnit(Enum):
    """
    Pressure unit types for the pressure gauges
    """
    Torr = 0
    MBar = 1
    Pascal = 2


class OptionalUnitsDisplay(Enum):
    """
    What to display on an optional Pressure Gauge display
    """
    Vacuum = 0
    Differential = 1
    Both = 2


class FilamentMode(Enum):
    """
    Sets the operational mode of the filament
    """
    Manual = 0
    Alternating = 1
    Automatic = 2
    Both = 3


class FilamentOperation(Enum):
    """
    Represents the operation of the two filaments in the Vacuum Chamber
    """
    FilamentOne = 0
    FilamentTwo = 1
    Both = 2
    Neither = 3


class CalibrationType(Enum):
    """
    The type of pressure calibration to run on the pressure gauge.
    """
    Atmosphere = 0
    Vacuum = 1


class PressureGauge(Protocol):
    """
    A protocol representing the different behaviors of a power supply
    """

    @property
    def vacuum_pressure(self) -> float:
        """Returns the current vacuum pressure reading in the chamber"""
        raise NotImplementedError()

    @property
    def differential_pressure(self) -> float:
        """Returns the current differential pressure reading (difference between ATM/CHMBR)"""
        raise NotImplementedError()

    @property
    def units(self) -> PressureUnit:
        """Returns the currently set pressure units in the pressure gauge"""
        raise NotImplementedError()

    @units.setter
    def units(self, value: PressureUnit):
        """Sets the current pressure unit type to use in the pressure gauge. Choices are Torr, MBAR, Pascal."""
        raise NotImplementedError()

    @property
    def micron_gauge(self) -> bool:
        """Returns if the micron gauge is active (True) or not (False)"""
        raise NotImplementedError()

    @micron_gauge.setter
    def micron_gauge(self, value: bool):
        """Sets the micron gauge ON or OFF"""
        raise NotImplementedError()

    @property
    def conductron_enabled(self) -> bool:
        """Determines if the pressure is read from a Conductron sensor when the Micron gauge is not active or not."""
        raise NotImplementedError()

    @conductron_enabled.setter
    def conductron_enabled(self, value: bool):
        """Sets if the conductron sensor is used when the micron gauge is not active."""
        raise NotImplementedError()

    @property
    def micron_gauge_on_delay_enabled(self) -> bool:
        """Queries if the Micron ON delay is enabled or not"""
        raise NotImplementedError()

    @micron_gauge_on_delay_enabled.setter
    def micron_gauge_on_delay_enabled(self, value: bool):
        """Sets if the Micron delay is enabled (True) or not"""
        raise NotImplementedError()

    @property
    def micron_gauge_on_delay_time(self) -> int:
        """
        Queries the amount of time to wait before enabling the micron gauge in seconds.
        Note if the `micron_gauge_on_delay_enabled`, this amount is added in addition to the delay determined by the
        pressure switch firmware.
        """
        raise NotImplementedError()

    @micron_gauge_on_delay_time.setter
    def micron_gauge_on_delay_time(self, value: int):
        """The minimum amount of time to wait before turning on the micron gauge."""
        raise NotImplementedError()

    @property
    def micron_filament_mode(self) -> FilamentMode:
        """Queries the status of filament modes"""
        raise NotImplementedError()

    @micron_filament_mode.setter
    def micron_filament_mode(self, value: FilamentMode):
        """Sets the filament operating mode of the pressure switch"""
        raise NotImplementedError()

    @property
    def micron_filament_status(self) -> FilamentOperation:
        """Returns the current operational status of the two filaments in the Vacuum Gauge"""
        raise NotImplementedError()

    @property
    def degas_micron_enabled(self) -> bool:
        """Queries if the micron gauge is in degas mode or not."""
        raise NotImplementedError()

    @degas_micron_enabled.setter
    def degas_micron_enabled(self, value: bool):
        """Sets if the micron gauge is in degas mode or not"""
        raise NotImplementedError()

    @property
    def degas_micron_time(self) -> int:
        """The amount of seconds to run the degas operation on the micron gauge."""
        raise NotImplementedError()

    @degas_micron_time.setter
    def degas_micron_time(self, value: int):
        """Sets the amount of seconds to run the degas operation on the micron gauge."""
        raise NotImplementedError()

    @property
    def emission(self) -> float:
        """Returns the low -> high emission current trip point in vacuum pressure."""
        raise NotImplementedError()

    @emission.setter
    def emission(self, value: float):
        """Sets the low -> high emission circuit trip point in vacuum pressure."""
        raise NotImplementedError()

    @property
    def emission_current(self) -> Optional[float]:
        """Reads the emission current of the micron-gauge"""
        raise NotImplementedError()

    def calibrate(self, cal_type: CalibrationType):
        """Calibrates the pressure gauge at Atmosphere or Vacuum."""
        raise NotImplementedError()

    @property
    def atmosphere_output(self) -> Optional[int]:
        """
        Returns if the ATM command is set, if None is returned, then the ACTUAL pressure is displayed when
        no difference is measured between atmosphere and vacuum chamber
        """
        raise NotImplementedError()

    @atmosphere_output.setter
    def atmosphere_output(self, value: Optional[int]):
        """Sets the measurement to show when there is no difference between chamber and outside."""
        raise NotImplementedError()

    def status(self) -> str:
        """Reads the status strings from the vacuum gauge"""
        raise NotImplementedError()

    def reset(self):
        """Resets the unit to the default power-on state."""
        raise NotImplementedError()

    def factory_reset(self):
        """Resets the NVRAM to the factory defaults, this *will* cause inaccurate readings until calibrated."""
        raise NotImplementedError()

    @property
    def version(self) -> str:
        """Returns the version string read out from the unit."""

    @abstractmethod
    def close(self):
        """Resets the PSU to a safe state."""
        raise NotImplementedError()
