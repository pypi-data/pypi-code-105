# Copyright 2021 Patrick C. Tapping
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.


from enum import Enum
from collections import namedtuple
from datetime import datetime
import re
import logging
import asyncio
from threading import Thread, Lock
from typing import Callable
from time import sleep

import serial
from serial.tools import list_ports


__version__ = "1.0.0"


class Ion3():
    """
    Initialise and open serial device for the SmartChem-Ion3 ion-selective electrode interface.

    The ``serial_port`` parameter may be a system-specific string (eg. ``"/dev/ttyUSB0"``,
    ``"COM12"``) or a :data:`~serial.tools.list_ports_common.ListPortInfo` instance. If the
    ``serial_port`` parameter is ``None`` (default), then an attempt to detect a serial device will
    be performed. The first device found will be initialised. If multiple serial devices are present
    on the system, then the use of the the additional keyword arguments can be used to select a
    specific device. The keyword arguments the same as those used for :meth:`find_device`.

    The communication baud rate should match that configured on the device. Options for the
    ``baudrate`` parameter are 1200, 9600, 19200, or 38400 (default).

    The device may send data back spontaneously (with out a specific request from the host) when
    configured to use its "Instant Send" or "Print" functions. The function specified by the
    ``data_callback`` parameter will be called and passed the data for each received data record.
    The callback function can be also configured after initialisation by setting the
    :data:`data_callback` property.

    :param serial_port: Serial port device the device is connected to.
    :param baudrate: Serial port baud rate to use.
    :param data_callback: Function to call on receipt of spontaneous data.
    :param vid: Numerical USB vendor ID to match.
    :param pid: Numerical USB product ID to match.
    :param manufacturer: Regular expression to match to a device manufacturer string.
    :param product: Regular expression to match to a device product string.
    :param serial_number: Regular expression to match to a device serial number.
    :param location: Regular expression to match to a device physical location (eg. USB port).
    """

    def __init__(self, serial_port=None, baudrate=38400, data_callback=None, **kwargs):
        
        # If serial_port not specified, search for a device
        if serial_port is None:
            serial_port = find_device(**kwargs)

        # Accept a serial.tools.list_ports.ListPortInfo object (which we may have just found)
        if isinstance(serial_port, serial.tools.list_ports_common.ListPortInfo):
            serial_port = serial_port.device
        
        if serial_port is None:
            raise RuntimeError("No devices detected matching the selected criteria.")

        self._log = logging.getLogger(__name__)
        self._log.debug(f"Initialising serial port ({serial_port}).")
        # Open and configure serial port settings
        self._port = serial.Serial(serial_port,
                                   baudrate=baudrate,
                                   bytesize=serial.EIGHTBITS,
                                   parity=serial.PARITY_NONE,
                                   stopbits=serial.STOPBITS_ONE,
                                   xonxoff=True,
                                   timeout=0.5,
                                   write_timeout=1.0,
                                )
        self._port.reset_input_buffer()
        self._port.reset_output_buffer()
        self._log.debug("Opened serial port OK.")
        
        # Lock on serial port to prevent simultaneous access
        self._lock = Lock()
        self._lock_timeout = 3.0

        # Fields populated by status updates
        self._firmware_version = "Unknown"
        self._serial_number = "Unknown"
        self._nreadings = 0

        # Send an status request to ensure device is correct and functioning
        try:
            self._update_status()
        except:
            raise RuntimeError("Error communicating with device. Check port, baudrate, power, not in menu etc.")

        # Callback function for receipt of spontaneous data
        self.data_callback = data_callback

        # Create a new event loop for ourselves, running in a separate thread
        self._eventloop = asyncio.new_event_loop()
        self._thread = Thread(target=self._run_eventloop, daemon=True)
        self._thread.start()

        # Duration between status update requests
        self._update_interval = 2.0
        # Status update task handle, start background status updates
        self._update_handle = self._eventloop.call_soon_threadsafe(self._background_update)

        # Duration between checks for new spontaneous data on serial port
        self._read_interval = 0.05
        # Port read task handle, start background checks for data
        self._read_handle = self._eventloop.call_soon_threadsafe(self._background_read)


    @property
    def serial_number(self) -> str:
        """
        Serial number of the device, as a string.
        """
        return self._serial_number
    
    @property
    def firmware_version(self) -> str:
        """
        Firmware version on the device, as a string.
        """
        return self._firmware_version

    @property
    def n_readings(self) -> int:
        """
        Number of logged readings in the device memory.
        """
        return self._nreadings

    @property
    def data_callback(self) -> Callable:
        """
        Function to call on receipt of spontaneous data from the device.
        """
        return self._data_callback
    
    @data_callback.setter
    def data_callback(self, cb) -> None:
        if cb is None:
            self._data_callback = lambda: None
        elif callable(cb):
            self._data_callback = cb
        else:
            # Ensure callback is always callable by using a null lambda function
            self._log.warning("Data callback is not a callable function, ignoring.")
            self._data_callback = lambda: None


    def _run_eventloop(self):
        """
        Run the thread for the event loop.
        """
        self._log.debug("Starting event loop.")
        asyncio.set_event_loop(self._eventloop)
        try:
            self._eventloop.run_forever()
        finally:
            self._eventloop.close()
        self._log.debug("Event loop stopped.")
        if self._port and self._port.is_open:
            try:
                self._port.close()
                self._log.debug("Closed serial connection.")
                self._lock.release()
            except:
                self._log.debug("Error closing serial connection.")


    def close(self) -> None:
        """
        Close the connection to the device.
        """
        # Cancel background updates and stop the event loop
        self._read_handle.cancel()
        self._update_handle.cancel()
        self._eventloop.stop()


    def _write_command(self, command_string:str, terminator="\r", timeout:float=None) -> str:
        """
        Write a command out the the serial port, wait for response, and return the received string.
        
        A carriage return will be appended to the given ``command_string``.

        The ``terminator`` can be specified, which is a string which indicates the end of the reply
        message. The terminator will be removed from the returned string.

        The ``timeout`` value is a time in seconds to wait to acquire the lock on the serial port.
        If the lock can't be acquired within this time, a :class:`~serial.SerialException` will be
        raised.
        """
        if not (self._port and self._port.is_open):
            raise serial.SerialException("Serial connection has been closed.")
        if timeout is None:
            timeout = self._lock_timeout
        if not self._lock.acquire(timeout=timeout):
            raise serial.SerialException("Unable to acquire lock for exclusive serial port access.")
        request_data = bytearray(f"{command_string}\r", "ascii")
        #self._log.debug(f"Writing command string: {request_data}")
        self._port.write(request_data)
        self._port.flush()
        indata = ""
        while not indata.endswith(terminator):
            try:
                inbytes = self._port.read(1)
            except serial.SerialException as ex:
                self._lock.release()
                raise serial.SerialException("Error reading response string.")
            if len(inbytes) > 0:
                indata += inbytes.decode("ascii")
            else:
                self._lock.release()
                raise serial.SerialException("Timeout reading response string.")
            # For multi-line responses, the computer must respond with a character after each new line.
            # This is annoying since this method doesn't know if the message is supposed to be multiline.
            # A carriage return is probably a good choice as it shouldn't mess things up if not needed.
            if indata[-1] == "\r":
                self._port.write(b"\r")
                self._port.flush()
        indata = indata.removesuffix(terminator).replace("\r", "\n")
        #self._log.debug(f"Received response string: {indata}")
        self._lock.release()
        return indata


    def _update_status(self):
        """
        Request the current status of the device.
        """
        #self._log.debug("Querying device status.")
        reply_data = self._write_command("?S", terminator="%\r")
        #self._log.debug(f"Status update returned: {reply_data}")
        # Parse the info string
        model, fw, serialno, nreadings = reply_data.split()
        if not model == "smartCHEM-I3":
            raise RuntimeError(f"Status request returned unexpected model string: '{model}'")
        self._firmware_version = fw
        self._serial_number = serialno
        self._nreadings = int(nreadings)


    def _background_update(self):
        """
        Request the current status of the device, then cue another request for later.
        """
        if not (self._port and self._port.is_open):
            return
        try:
            self._update_status()
        except serial.SerialException:
            self._log.debug("Timeout during status update, device may be busy in menu.")
        except Exception as ex:
            self._log.exception("Error updating status from device.")
            # TODO: Could try to reset/recover etc.
        self._update_handle = self._eventloop.call_later(self._update_interval, self._background_update)


    def _background_read(self):
        """
        Check the serial port for any data sent spontaneously by the device.
        """
        if not (self._port and self._port.is_open):
            return
        # Don't interrupt comms if port already in use
        if not self._lock.locked() and self._port.in_waiting > 0 and self._lock.acquire(timeout=self._read_interval):
            # Keep reading if there is data waiting in the input buffer
            while self._port.in_waiting:
                # Data lines should be 69 chars followed by CRLF
                line = self._port.read_until(expected="\r\n", size=71)
                if len(line) != 71 or line[-2:] != b"\r\n":
                    if line[:12] == b"smartCHEM-I3":
                        # Could be a missed status update, ignore it
                        continue
                    elif line[:4] == b"ENDS":
                        # End of logged data lines, ignore it
                        continue
                    self._log.debug(f"Couldn't read spontaneous data message, received:\n{line}")
                    continue
                try:
                    data = _parse_data_line(line.decode("ascii"))
                except:
                    self._log.warn(f"Couldn't decode spontaneous data message, received:\n{line}")
                    continue
                # Call the data callback with data from this line
                self._log.debug(f"Received spontaneous data: {data}")
                self._data_callback(data)
                # The device is really slow, we'll wait a bit to see if it starts sending
                # another line of data as part of the logged data messages
                sleep(0.05)
            self._lock.release()
        # Cue up next check for spontaneous data on serial port
        self._read_handle = self._eventloop.call_later(self._read_interval, self._background_read)


    def current_data(self):
        """
        Get the current data readings from the device.

        :returns: A single reading from the device as a :class:`~Data` instance.
        """
        try:
            reply = self._write_command("?D")
            return _parse_data_line(reply)
        except:
            raise RuntimeError("Error reading data from device.")
        

    def logged_data(self) -> list:
        """
        Get the set of logged data readings from the device.

        :returns: A list of readings from the device as :class:`~Data` instances.
        """
        try:
            reply = self._write_command("?R", terminator="ENDS\r")
            data = []
            for line in reply.split("\r"):
                if line:
                    data.append(_parse_data_line(line))
            return data
        except:
            raise RuntimeError("Error reading logged data from device.")


    def erase_log(self) -> None:
        """
        Erase any logged data records stored on the device.
        """
        try:
            self._write_command("?E", terminator="ERASED\r")
        except:
            raise RuntimeError("Error erasing logged data from device.")


    def glp(self) -> str:
        """
        Get the "Good Laboratory Practices" table containing the device's calibration information.

        The table is returned as raw ASCII as specified in the device documentation (no attempt is
        made to parse the individual fields).

        :returns: Good Laboratory Practices table as a string.
        """
        return self._write_command("?G", terminator="\rENDS\r")


class Unit(Enum):
    """
    An Enum to assist with matching and displaying the unit types used by the device.
    """

    PH = "pH"
    MV = "mV"
    MVR = "mVR"
    PPM = "ppM"
    PPK = "ppK"
    PERCENT = "%"
    EXP = ""
    UNCAL = "UnCal"
    C = "oC"
    CM = "oCm"

    @property
    def description(self):
        """
        Return a string describing the type of unit.
        """
        return {
            Unit.PH : "pH",
            Unit.MV : "millivolts (absolute)",
            Unit.MVR : "millivolts (relative)",
            Unit.PPM : "parts per million",
            Unit.PPK : "parts per thousand",
            Unit.PERCENT : "percent",
            Unit.EXP : "exponential",
            Unit.UNCAL : "uncalibrated, arbitrary units",
            Unit.C : "degrees Celsius",
            Unit.CM : "degrees Celsius (manual compensation)",
        }[self]
    
    @property
    def suffix(self):
        """
        Return a string format of the unit's suffix to append to a value.
        """
        return {
            Unit.PH : "",
            Unit.MV : " mV",
            Unit.MVR : " mV",
            Unit.PPM : " ppm",
            Unit.PPK : " ppk",
            Unit.PERCENT : "%",
            Unit.EXP : "",
            Unit.UNCAL : " (a.u.)",
            Unit.C : " ℃",
            Unit.CM : " ℃",
        }[self]
        

#: A namedtuple containing a single reading from a single channel, consiting of a value and its units.
ChannelData = namedtuple("ChannelData", "value, unit", defaults=[0.0, Unit.UNCAL])
ChannelData.value.__doc__ = "Value for the data reading."
ChannelData.unit.__doc__ = "Unit associated with the data reading, as a :data:`~Unit` object."

#: A namedtuple containing a single reading from the device, consisting of three channels plus temperature data.
#: Each of the channel entries is an instance of :data:`~ChannelData`.
Data = namedtuple("Data", "ch1, ch2, ch3, cht, timestamp, n", defaults=[
    ChannelData(0.0, Unit.UNCAL),
    ChannelData(0.0, Unit.UNCAL),
    ChannelData(0.0, Unit.UNCAL),
    ChannelData(0.0, Unit.C),
    datetime.now().astimezone(),
    0,
])
Data.ch1.__doc__ = "Probe channel 1 data as a :data:`~ChannelData` object."
Data.ch2.__doc__ = "Probe channel 2 data as a :data:`~ChannelData` object."
Data.ch3.__doc__ = "Probe channel 3 data as a :data:`~ChannelData` object."
Data.cht.__doc__ = "Temperature channel data as a :data:`~ChannelData` object."
Data.timestamp.__doc__ = "Timestamp of data reading as a python ``datetime`` object."
Data.n.__doc__ = "Index of data reading."


def _parse_data_line(data_line):
    """
    Parse a string containing a line of data into a :class:`~Data` instance.
    """
    #d, t, n, ch1, ch2, ch3, cht = data_line.split()
    dt = datetime.strptime(data_line[0:19], "%d/%m/%Y %H:%M:%S").astimezone()
    n = int(data_line[20:24])
    ch1 = ChannelData(float(data_line[25:33].replace("*", ".").replace("OVR", "nan")), Unit(data_line[33:36].strip()))
    ch2 = ChannelData(float(data_line[37:45].replace("*", ".").replace("OVR", "nan")), Unit(data_line[45:48].strip()))
    ch3 = ChannelData(float(data_line[49:57].replace("*", ".").replace("OVR", "nan")), Unit(data_line[57:60].strip()))
    cht = ChannelData(float(data_line[61:66].replace("*", ".").replace("OVR", "nan")), Unit(data_line[66:69].strip()))
    return Data(ch1, ch2, ch3, cht, dt, n)


def find_device(vid=None, pid=None, manufacturer=None, product=None, serial_number=None, location=None):
    """
    Search attached serial ports for a specific device.

    The first device found matching the criteria will be returned.
    Because there is no consistent way to identify serial devices, the default parameters do not
    specify any selection criteria, and thus the first serial port will be returned.
    A specific device should be selected using a unique combination of the parameters.

    The USB vendor (``vid``) and product (``pid``) IDs are exact matches to the numerical values,
    for example ``vid=0x067b`` or ``vid=0x2303``. The remaining parameters are strings specifying a
    regular expression match to the corresponding field. For example ``serial_number="83"`` would
    match devices with serial numbers starting with 83, while ``serial_number=".*83$"`` would match
    devices ending in 83. A value of ``None`` means that the parameter should not be considered,
    however an empty string value (``""``) is subtly different, requiring the field to be present,
    but then matching any value.

    Be aware that different operating systems may return different data for the various fields, 
    which can complicate matching when attempting to write cross-platform code.

    To see a list of serial ports and the relevant data fields:

    .. code-block: python

        import serial
        for p in list_ports.comports():
            print(f"{p.device}, {p.manufacturer}, {p.product}, {p.vid}, {p.pid}, {p.serial_number}, {p.location}")

    :param vid: Numerical USB vendor ID to match.
    :param pid: Numerical USB product ID to match.
    :param manufacturer: Regular expression to match to a device manufacturer string.
    :param product: Regular expression to match to a device product string.
    :param serial_number: Regular expression to match to a device serial number.
    :param location: Regular expression to match to a device physical location (eg. USB port).
    :returns: First :class:`~serial.tools.list_ports.ListPortInfo` device which matches given criteria.
    """
    for p in list_ports.comports():
        if (vid is not None) and not vid == p.vid: continue
        if (pid is not None) and not pid == p.pid: continue
        if (manufacturer is not None) and ((p.manufacturer is None) or not re.match(manufacturer, p.manufacturer)): continue
        if (product is not None) and ((p.product is None) or not re.match(product, p.product)): continue
        if (serial_number is not None) and ((p.serial_number is None) or not re.match(serial_number, p.serial_number)): continue
        if (location is not None) and ((p.location is None) or not re.match(location, p.location)): continue
        return p


def list_devices():
    """
    Return a string listing all detected serial devices and any associated identifying properties.

    The manufacturer, product, vendor ID (vid), product ID (pid), serial number, and physical
    device location are provided.
    These can be used as parameters to :meth:`find_device` or the constructor of a device class
    to identify and select a specific serial device.

    :returns: String listing all serial devices and their details.
    """
    result = ""
    for p in list_ports.comports():
        try:
            vid = f"{p.vid:#06x}"
            pid = f"{p.pid:#06x}"
        except:
            vid = p.vid
            pid = p.pid
        result += f"device={p.device}, manufacturer={p.manufacturer}, product={p.product}, vid={vid}, pid={pid}, serial_number={p.serial_number}, location={p.location}\n"
    return result.strip("\n")
