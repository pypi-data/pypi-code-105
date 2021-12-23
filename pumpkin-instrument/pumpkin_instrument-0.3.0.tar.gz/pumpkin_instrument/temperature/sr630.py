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
Implementation of the protocol necessary to control the SR630 temperature
sensors
"""
import time
from typing import Optional, List, ContextManager, Any
from contextlib import contextmanager

from .types import ThermocoupleType, TemperatureUnit, TemperatureSensor
from .. import InstrumentType
from ..prologix import PrologixController
from ..instrument import Instrument

SR630_NUM_CH = 16
SR630_UNITS = {
    TemperatureUnit.Kelvin: "ABS",
    TemperatureUnit.Celcius: "CENT",
    TemperatureUnit.Farenheit: "FHRN",
    TemperatureUnit.Voltage: "DC"
}
SR630_THERMOCOUPLES = {
    ThermocoupleType.R: "R",
    ThermocoupleType.S: "S",
    ThermocoupleType.B: "B",
    ThermocoupleType.E: "E",
    ThermocoupleType.J: "J",
    ThermocoupleType.K: "K",
    ThermocoupleType.T: "T"
}
SR630_TEMP_RANGE = [-270, 3300]


class _SR630Context(TemperatureSensor):
    def __init__(self, prologix: PrologixController, address: int):
        """
        Initializes the SR630 context with the given prologix controller, ensuring:

        * Unit is RST and alarms are cleared
        * Units are set to Celsius by default

        :param prologix: The Prologix controller
        :param address: The address on the GPIB bus of the thermocouple device
        """
        self.prologix = prologix
        self.address = address

        # Send *RST command
        self._write_cmd('*RST')

        for i in range(1, SR630_NUM_CH):
            # Reset all of the alarms to NO status
            self.set_alarm(i)
            # Set all channels to C
            self.set_units(i, TemperatureUnit.Celcius)
            # Default to T type thermocouples for the TVAC chamber
            self.set_thermocouple_type(i, ThermocoupleType.T)
        self.prologix.selected_device_clear(self.address)

    def _write_read_cmd(self, cmd: str, timeout: float = 0.5) -> bytes:
        """
        Writes a command, then immediately tries to read back a response, waiting up to `timeout`
        seconds for the unit to respond.
        """
        self._write_cmd(cmd)
        time.sleep(0.08)
        return self.prologix.read_until(self.address, timeout=timeout)

    def _write_cmd(self, cmd: str):
        """Writes a single command to the thermocouple sensor with proper encoding"""
        self.prologix.write(self.address, cmd.encode('ascii') + b'\n')

    @staticmethod
    def _verify_temp_range(temperature: float):
        """Raises an exception if the temperature is out of range for the unit."""
        if temperature < SR630_TEMP_RANGE[0] or temperature > SR630_TEMP_RANGE[1]:
            raise ValueError(f"Invalid temperature: {temperature}, must be in range {SR630_TEMP_RANGE}")

    def set_units(self, ch: int, units: TemperatureUnit):
        """Sets the units to use on `ch` to `units`."""
        if units not in SR630_UNITS:
            raise ValueError(f'{units} is not supported on the SR630')
        self._write_cmd(f'UNIT {ch},{SR630_UNITS[units]}')

    def measure_temp(self, ch: int) -> float:
        """Measures the temperature of the given `ch` in the units set for the channel."""
        try:
            read = self._write_read_cmd(f'MEAS? {ch}')
        except RuntimeError:
            read = self._write_read_cmd(f'MEAS? {ch}', timeout=1.0)
        try:
            return float(read)
        except ValueError as e:
            self._write_cmd('BCLR')
            self.prologix.selected_device_clear(self.address)
            raise RuntimeError(f'Unexpected response: {read}')

    def set_alarm(self, ch: int, low_temp: Optional[float] = None, high_temp: Optional[float] = None):
        """
        Sets the alarm functionality of the temperature sensor unit to trigger.

        N.B. if `low_temp` or `high_temp` is set to None, then the alarm is defined as an `upper` or `lower` limit
        respectively. If both are None, then the alarm is disabled.

        :param ch: The channel to set the alarm for
        :param low_temp: The lower bound for the alarm
        :param high_temp: The upper bound for the alarm
        """
        if low_temp is None and high_temp is None:
            self._write_cmd(f'ALRM {ch},NO')
        else:
            if low_temp:
                self._verify_temp_range(low_temp)
                self._write_cmd(f'TMIN {ch},{low_temp}')
            else:
                self._write_cmd(f'TMIN {ch},{SR630_TEMP_RANGE[0]}')
            if high_temp:
                self._verify_temp_range(high_temp)
                self._write_cmd(f'TMAX {ch},{high_temp}')
            else:
                self._write_cmd(f'TMAX {ch},{SR630_TEMP_RANGE[1]}')
            self._write_cmd(f'ALRM {ch},YES')

    def get_alarms(self) -> List[bool]:
        """
        Gets the list of alarms that are present on the temperature sensor.
        N.B. this will clear the current list of alarms that are trigger on the temperature sensor.
        """
        resp = self._write_read_cmd(f'ALRM?')
        try:
            resp = int(resp)
        except ValueError:
            self.prologix.selected_device_clear(self.address)
            raise RuntimeError(f'Unexcpected response: {resp}')
        return [digit == '1' for digit in bin(resp)[2:]]

    def set_thermocouple_type(self, ch: int, thermocouple_type: ThermocoupleType):
        if thermocouple_type not in SR630_THERMOCOUPLES:
            raise RuntimeError(f'{thermocouple_type} is not supported on the SR630')
        self._write_cmd(f'TTYP {ch},{SR630_THERMOCOUPLES[thermocouple_type]}')


class SR630(Instrument):
    def __init__(self, prologix: PrologixController, address: int):
        """Stores the configuration necessary to initialize the SR630 instrument."""
        self.prologix = prologix
        self.address = address

    @classmethod
    def instrument_type(cls) -> InstrumentType:
        """Returns `Thermocouple`"""
        return InstrumentType.Thermocouple

    @classmethod
    def instrument_capabilities(cls) -> Any:
        return None

    @classmethod
    def channel_capabilities(cls) -> List[Any]:
        return []

    @contextmanager
    def use(self) -> ContextManager[Any]:
        """Initializes the SR630 for usage"""
        temp_sensor = _SR630Context(self.prologix, self.address)
        yield temp_sensor
