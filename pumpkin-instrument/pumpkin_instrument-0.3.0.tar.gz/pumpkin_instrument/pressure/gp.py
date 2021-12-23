# coding: utf-8
# ##############################################################################
#  (C) Copyright 2020 Pumpkin, Inc. All Rights Reserved.                       #
#                                                                              #
#  This file may be distributed under the terms of the License                 #
#  Agreement provided with this software.                                      #
#                                                                              #
#  THIS FILE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND,                   #
#  INCLUDING THE WARRANTY OF DESIGN, MERCHANTABILITY AND                       #
#  FITNESS FOR A PARTICULAR PURPOSE.                                           #
# ##############################################################################
"""
Implementation for the GP390 Micro-Ion Pressure Gauge
"""
from typing import Optional, List, Tuple, ContextManager, Any
from contextlib import contextmanager

import serial
import io
import logging

from .types import PressureUnit, PressureGauge, CalibrationType, OptionalUnitsDisplay, FilamentMode, FilamentOperation
from .. import Instrument, InstrumentType

logger = logging.getLogger(__name__)

GP390_UNITS_RESP = {
    "TORR": PressureUnit.Torr,
    "MBAR": PressureUnit.MBar,
    "PASCAL": PressureUnit.Pascal
}
GP390_UNITS_CMD = {
    PressureUnit.Torr: "SUT",
    PressureUnit.MBar: "SUM",
    PressureUnit.Pascal: "SUP"
}
GP390_FILAMENT_MODE = {
    FilamentMode.Manual: "SFMAN",
    FilamentMode.Automatic: "SFAUTO",
    FilamentMode.Both: "SFBOTH",  # TODO: Figure out if this is correct ...
    FilamentMode.Alternating: "SFALT"
}
GP390_CAL_CMD = {
    CalibrationType.Vacuum: "TZ",
    CalibrationType.Atmosphere: "TS"
}


class RS485Adapter:
    """Implements the RS485 protocol needed for the GP390 pressure gauge"""
    def __init__(self, port: str, baudrate=19200, timeout=1.0):
        """Initializes a RS485 adapter to send/receive commands from the GP390 unit"""
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))
        logger.info(f"Opened {port}@{baudrate} with a timeout of {timeout:0.3f} seconds.")

    def send_cmd(self, addr: int, cmd: str) -> str:
        """Sends `cmd` to the RS485 device at `addr`. Returns the response separated by newline."""
        cmd = f"#{addr:02X}{cmd}\x0D"
        logger.info(f'sending: {cmd}')
        self.sio.write(str(cmd))
        self.sio.flush()
        return self.sio.readline()

    def close(self):
        """Closes the serial port and buffered IO"""
        self.sio.close()
        self.ser.close()


class _GP390PressureGaugeContext(PressureGauge):
    """Represents the running context of the GP390 pressure gauge unit."""
    def __init__(self, adapter: RS485Adapter, addr: int):
        self.adapter = adapter
        self.addr = addr

    def _write_read_tokens(self, cmd: str) -> Tuple[List[str], str]:
        """Writes a command, returns an array split by whitespace."""
        resp = self.adapter.send_cmd(self.addr, cmd)
        return resp.split(), resp

    def _send_verify_cmd(self, cmd: str) -> Tuple[bool, str]:
        """Sends a command, verifying PROGM OK is in response"""
        resp = self.adapter.send_cmd(self.addr, cmd)
        if 'LOCKED' in resp:
            lock_resp = self.adapter.send_cmd(self.addr, "TLU")
            if 'OFF' not in lock_resp:
                raise RuntimeError(f'Failed to unlock the device... got: {lock_resp}')
            resp = self.adapter.send_cmd(self.addr, cmd)
        return 'PROGM OK' in resp, resp

    @property
    def vacuum_pressure(self) -> float:
        """Gets the vacuum pressure in the currently set units"""
        elements, resp = self._write_read_tokens('RD')
        try:
            return float(elements[1])
        except ValueError:
            raise ValueError(f'Failed to read vacuum pressure, got: {resp}')
        except IndexError:
            raise ValueError(f'Failed to read vacuum pressure, got: {resp}')

    @property
    def differential_pressure(self) -> float:
        """Gets the differential pressure, or the difference between atmosphere and vacuum."""
        elements, resp = self._write_read_tokens('RDD')
        try:
            return float(elements[1])
        except ValueError:
            raise ValueError(f'Failed to read differential vacuum pressure, got: {resp}')
        except IndexError:
            raise ValueError(f'Failed to read differential vacuum pressure, got: {resp}')

    @property
    def units(self) -> PressureUnit:
        """Gets the currently set units"""
        elements, resp = self._write_read_tokens("RU")
        try:
            return GP390_UNITS_RESP[elements[1]]
        except KeyError:
            raise ValueError(f'Failed to read units, got: {resp}')

    @units.setter
    def units(self, value: PressureUnit):
        """Sets the units to use for the pressure gauge"""
        ok, resp = self._send_verify_cmd(GP390_UNITS_CMD[value])
        if not ok:
            raise RuntimeError(f'Failed to set units, got: {resp}')

    @property
    def micron_gauge(self) -> bool:
        """Reads the state of the micron gauge"""
        resp = self.adapter.send_cmd(self.addr, "IGS")
        if "ON" in resp:
            return True
        elif "OFF" in resp:
            return False
        else:
            raise RuntimeError(f'Unexpected response: {resp}')

    @micron_gauge.setter
    def micron_gauge(self, value: bool):
        """Sets the state of the micron gauge to ON"""
        ok, resp = self._send_verify_cmd(f'IG{1 if value else 0}')
        if not ok:
            raise RuntimeError(f'Failed to turn on Micron Gauge, got: {resp}')

    @property
    def conductron_enabled(self) -> bool:
        """Returns if the conductron sensor is enabled when the micron gauge is off"""
        resp = self.adapter.send_cmd(self.addr, "IGMS")
        if "ALL" in resp:
            return True
        if "IG" in resp:
            return False
        else:
            raise RuntimeError(f'Unexpected response: {resp}')

    @conductron_enabled.setter
    def conductron_enabled(self, value: bool):
        """Sets if the conductron sensor is enabled when the micron gauge is off"""
        ok, resp = self._send_verify_cmd(f'IGM{1 if value else 0}')
        if not ok:
            raise RuntimeError(f'Failed to set conductron on, got: {resp}')

    @property
    def micron_gauge_on_delay_enabled(self) -> bool:
        """Gets if the micron gauge on delay is enabled (IOD)"""
        resp = self.adapter.send_cmd(self.addr, "IOD")
        if "ON" in resp:
            return True
        elif "OFF" in resp:
            return False
        else:
            raise RuntimeError(f'Unexpected response for IOD: {resp}')

    @micron_gauge_on_delay_enabled.setter
    def micron_gauge_on_delay_enabled(self, value: bool):
        """Sets if the micron gauge on delay is enabled or not (IOD#)"""
        ok, resp = self._send_verify_cmd(f"IOD{1 if value else 0}")
        if not ok:
            raise RuntimeError(f'Failed to set micron gauge on delay, got: {resp}')

    @property
    def micron_gauge_on_delay_time(self) -> int:
        """Gets the micron gauge on delay time in seconds."""
        elements, resp = self._write_read_tokens("IDT")
        try:
            return int(elements[1])
        except ValueError:
            raise RuntimeError(f'Unexpected response for reading micron gauge on delay, got: {resp}')

    @micron_gauge_on_delay_time.setter
    def micron_gauge_on_delay_time(self, value: int):
        """Sets the micron gauge on delay time in seconds"""
        ok, resp = self._send_verify_cmd(f"IDT {value}")
        if not ok:
            raise RuntimeError(f"Failed to set the Micron gauge on delay time, got: {resp}")

    @property
    def micron_filament_mode(self) -> FilamentMode:
        """Gets the micron gauge filament mode in use"""
        raise NotImplementedError('Unable to query filament mode -- no command available in GP390')

    @micron_filament_mode.setter
    def micron_filament_mode(self, value: FilamentMode):
        """Sets the micron gauge filament operating mode"""
        try:
            ok, resp = self._send_verify_cmd(f'{GP390_FILAMENT_MODE[value]}')
            if not ok:
                raise RuntimeError(f"Failed to set micron gauge filament mode, got: {resp}")
        except KeyError:
            raise ValueError(f'Unsupported mode: {value}')

    @property
    def micron_filament_status(self) -> FilamentOperation:
        """Returns the current operational status of the two filaments in the Vacuum Gauge"""
        resp = self.adapter.send_cmd(self.addr, 'RF')
        if "SF1" in resp:
            return FilamentOperation.FilamentOne
        elif "SF2" in resp:
            return FilamentOperation.FilamentTwo
        elif "SFB" in resp:
            return FilamentOperation.Both
        else:
            raise RuntimeError(f'Unexpected response for querying filament status: {resp}')

    @property
    def degas_micron_enabled(self) -> bool:
        """Gets if degas micron gauge is enabled"""
        resp = self.adapter.send_cmd(self.addr, 'DGS')
        if "ON" in resp:
            return True
        elif "OFF" in resp:
            return False
        else:
            raise RuntimeError(f'Unexpected response for querying degas state: {resp}')

    @degas_micron_enabled.setter
    def degas_micron_enabled(self, value: bool):
        """Sets if the degas micron gauge is enabled"""
        ok, resp = self._send_verify_cmd(f'DG{1 if value else 0}')
        if not ok:
            raise RuntimeError(f'Unexpected response for enabling/disabling degas micron gauge: {resp}')

    @property
    def degas_micron_time(self) -> int:
        """Gets the amount of time for degassing the micron gauge."""
        elements, resp = self._write_read_tokens("DGT")
        try:
            return int(elements[1])
        except ValueError:
            raise RuntimeError(f'Unexpected response for reading degas time: {resp}')

    @degas_micron_time.setter
    def degas_micron_time(self, value: int):
        ok, resp = self._send_verify_cmd(f'DGT{value}')
        if not ok:
            raise RuntimeError(f'Unexpected response for setting degas time: {resp}')

    @property
    def emission(self) -> float:
        """Reads the emission trip point of the micron gauge"""
        elements, resp = self._write_read_tokens("SER")
        try:
            return float(elements[1])
        except ValueError:
            raise RuntimeError(f'Unexpected response for reading emission trip point: {resp}')

    @emission.setter
    def emission(self, value: float):
        """Sets the emission trip point of the micron gauge"""
        ok, resp = self._send_verify_cmd(f"SER {value:.2E}")
        if not ok:
            raise RuntimeError(f"Failed to set emission trip point: {resp}")

    @property
    def emission_current(self) -> Optional[float]:
        """Reads the emission current from the device"""
        elements, resp = self._write_read_tokens("RE")
        if "OFF" in resp:
            return None
        elif 'MA' not in resp:
            raise RuntimeError(f'Unexpected response for reading emission current: {resp}')
        token = elements[1]
        token = elements[:token.index('M')]
        try:
            return float(token)
        except ValueError:
            raise RuntimeError(f'Unexpected parse error for reading emission current: {resp}')

    def calibrate(self, cal_type: CalibrationType):
        """Sends the calibrate command to the GP390 pressure unit"""
        try:
            ok, resp = self._send_verify_cmd(GP390_CAL_CMD[cal_type])
        except KeyError:
            raise ValueError(f"Unsupported cal_type: {cal_type}")
        if not ok:
            raise RuntimeError(f"Calibration failed: {resp}")

    @property
    def atmosphere_output(self) -> Optional[int]:
        """Gets if the atmosphere output is set"""
        elements, resp = self._write_read_tokens("ATMS")
        if "ACTUAL" in resp:
            return None
        try:
            return int(elements[1])
        except ValueError:
            raise RuntimeError(f"Failed to read atmosphere output, got: {resp}")

    @atmosphere_output.setter
    def atmosphere_output(self, value: Optional[int]):
        """Sets the atmosphere output value, if None, sets to ACTUAL"""
        if value is None:
            cmd = "ATM ACTUAL"
        else:
            cmd = f"ATM {value}"
        ok, resp = self._send_verify_cmd(cmd)
        if not ok:
            raise RuntimeError(f"Failed to set atmosphere output, got: {resp}")

    def status(self) -> str:
        """Reads the status string of the pressure gauge"""
        return self.adapter.send_cmd(self.addr, "RS")

    def reset(self):
        """Sends the RST to reset to power on status."""
        self.adapter.send_cmd(self.addr, "RST")

    def factory_reset(self):
        """Sends the FAC command to reset to factory defaults"""
        ok, resp = self._send_verify_cmd("FAC")
        if not ok:
            raise RuntimeError(f'Failed to reset to factory defaults, got: {resp}')

    def send_custom_cmd(self, cmd: str) -> str:
        """Sends a custom command to the pressure unit, returning the response"""
        return self.adapter.send_cmd(self.addr, cmd)

    def close(self):
        """Closes the connection to the adapter"""
        self.adapter.close()


class GP390(Instrument):
    """Instrument implementation for the GP390 pressure gauge."""
    def __init__(self, adapter: RS485Adapter, addr: int):
        self.adapter = adapter
        self.addr = addr

    @classmethod
    def instrument_type(cls) -> InstrumentType:
        """Returns `PressureGauge`"""
        return InstrumentType.PressureGauge

    @classmethod
    def instrument_capabilities(cls) -> Any:
        return None

    @classmethod
    def channel_capabilities(cls) -> List[Any]:
        return []

    @contextmanager
    def use(self) -> ContextManager[Any]:
        cxt = _GP390PressureGaugeContext(self.adapter, self.addr)
        yield cxt
