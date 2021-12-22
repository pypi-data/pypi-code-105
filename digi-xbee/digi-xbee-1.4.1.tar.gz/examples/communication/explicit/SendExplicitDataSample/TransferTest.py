# Copyright 2017, Digi International Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from digi.xbee.devices import ZigBeeDevice

# TODO: Replace with the serial port where your local module is connected to.
from digi.xbee.exception import XBeeException, TimeoutException, ATCommandException
from digi.xbee.models.atcomm import ATStringCommand
from digi.xbee.models.status import TransmitStatus
from digi.xbee.packets.aft import ApiFrameType
from digi.xbee.packets.common import ExplicitAddressingPacket, TransmitPacket
from digi.xbee.serial import FlowControl
from threading import Event

import enum
import time

#PORT = "/dev/ttyXBee"
PORT = "/dev/ttyUSB3"
# TODO: Replace with the baud rate of your local module.
#BAUD_RATE = 921600
BAUD_RATE = 230400

REMOTE_NODE_ID = "DAVID_ROUTER_1"

_EXPLICIT_PACKET_BROADCAST_RADIUS_MAX = 0x00
_EXPLICIT_PACKET_CLUSTER_DATA = 0x0011
_EXPLICIT_PACKET_CLUSTER_LOOPBACK = 0x0012
_EXPLICIT_PACKET_ENDPOINT_DATA = 0xE8
_EXPLICIT_PACKET_EXTENDED_TIMEOUT = 0x40
_EXPLICIT_PACKET_PROFILE_DIGI = 0xC105

_PARAMETER_READ_RETRIES = 3
_PARAMETER_SET_RETRIES = 3


class _TransmitTest(object):
    """
    Helper class used to perform a transmit test between a local and a remote device.
    """

    _TEST_DATA = "This is the test data to send to the remote device during the 'Transmit Test'"

    def __init__(self, local_device, remote_device, num_packets=500):
        """
        Class constructor. Instantiates a new :class:`._LoopbackTest` with the given parameters.

        Args:
            local_device (:class:`.XBeeDevice`): local device to perform the loopback test with.
            remote_device (:class:`.RemoteXBeeDevice`): remote device against which to perform the loopback test.
            num_packets (Integer, optional): number of packets to transfer in the test. Defaults to 500. Set to -1
                                             for a continuous transfer test.
        """
        self._local_device = local_device
        self._remote_device = remote_device
        self._num_packets = num_packets
        self._total_packets_sent = 0
        self._total_packets_received = 0
        self._frame_id = 1

    def _generate_packet(self):
        packet = TransmitPacket(self._frame_id,
                                self._remote_device.get_64bit_addr(),
                                self._remote_device.get_16bit_addr(),
                                _EXPLICIT_PACKET_BROADCAST_RADIUS_MAX,
                                _EXPLICIT_PACKET_EXTENDED_TIMEOUT,
                                rf_data=self._TEST_DATA.encode())
        return packet

    def _transmit_callback(self, xbee_frame):
        if xbee_frame.get_frame_type() == ApiFrameType.TRANSMIT_STATUS:
            self._total_packets_received += 1

    def execute_test(self):
        """
        Performs the loopback test.

        Returns:
            Boolean: `True` if the test succeed, `False` otherwise.
        """
        print("Executing transmit test against %s" % self._remote_device)
        # Clear vars.
        self._frame_id = 1
        self._total_packets_sent = 0
        self._total_packets_received = 0
        # Add callback.
        self._local_device.add_packet_received_callback(self._transmit_callback)
        # Perform the loops test.
        while self._total_packets_sent < self._num_packets or self._num_packets < 0:
            try:
                # Send frame.
                self._local_device.send_packet(self._generate_packet())
                self._total_packets_sent += 1
                self._frame_id += 1
                if self._frame_id > 255:
                    self._frame_id = 1
            except XBeeException as e:
                print("Could not send test packet %s: %s" % (self._total_packets_sent + 1, str(e)))
        # Wait a couple of seconds to receive pending packets.
        time.sleep(2)
        # Remove frame listener.
        self._local_device.del_packet_received_callback(self._transmit_callback)
        # Return test result.
        print("Transfer test result: %s packets received out of %s" % (self._total_packets_received,
                                                                       self._total_packets_sent))
        return self._total_packets_received == self._total_packets_sent


class _LoopbackTest(object):
    """
    Helper class used to perform a loopback test between a local and a remote device.
    """

    _LOOPBACK_DATA = "Loopback test %s"

    def __init__(self, local_device, remote_device, loops=10, failures_allowed=10, timeout=2):
        """
        Class constructor. Instantiates a new :class:`._LoopbackTest` with the given parameters.

        Args:
            local_device (:class:`.XBeeDevice`): local device to perform the loopback test with.
            remote_device (:class:`.RemoteXBeeDevice`): remote device against which to perform the loopback test.
            loops (Integer, optional): number of loops to execute in the test. Defaults to 10.
            failures_allowed (Integer, optional): number of allowed failed loops before considering the test failed.
                                                  Defaults to 1.
            timeout (Integer, optional): the timeout in seconds to wait for the loopback answer. Defaults to 2 seconds.
        """
        self._local_device = local_device
        self._remote_device = remote_device
        self._num_loops = loops
        self._failures_allowed = failures_allowed
        self._loopback_timeout = timeout
        self._receive_lock = Event()
        self._packet_sent = False
        self._packet_received = False
        self._loop_failed = False
        self._total_loops_failed = 0
        self._frame_id = 1

    def _generate_loopback_packet(self):
        packet = ExplicitAddressingPacket(self._frame_id,
                                          self._remote_device.get_64bit_addr(),
                                          self._remote_device.get_16bit_addr(),
                                          _EXPLICIT_PACKET_ENDPOINT_DATA,
                                          _EXPLICIT_PACKET_ENDPOINT_DATA,
                                          _EXPLICIT_PACKET_CLUSTER_LOOPBACK,
                                          _EXPLICIT_PACKET_PROFILE_DIGI,
                                          _EXPLICIT_PACKET_BROADCAST_RADIUS_MAX,
                                          _EXPLICIT_PACKET_EXTENDED_TIMEOUT,
                                          (self._LOOPBACK_DATA % self._frame_id).encode())
        return packet

    def _loopback_callback(self, xbee_frame):
        if xbee_frame.get_frame_type() == ApiFrameType.TRANSMIT_STATUS and xbee_frame.frame_id == self._frame_id:
            if xbee_frame.transmit_status == TransmitStatus.SUCCESS:
                self._packet_sent = True
            else:
                self._receive_lock.set()
        elif (xbee_frame.get_frame_type() == ApiFrameType.EXPLICIT_RX_INDICATOR
              and xbee_frame.source_endpoint == _EXPLICIT_PACKET_ENDPOINT_DATA
              and xbee_frame.dest_endpoint == _EXPLICIT_PACKET_ENDPOINT_DATA
              and xbee_frame.cluster_id == _EXPLICIT_PACKET_CLUSTER_DATA
              and xbee_frame.profile_id == _EXPLICIT_PACKET_PROFILE_DIGI
              and xbee_frame.x64bit_source_addr == self._remote_device.get_64bit_addr()):
            # If frame was already received, ignore this frame, just notify.
            if self._packet_received:
                self._receive_lock.set()
                return
            # Check received payload.
            payload = xbee_frame.rf_data
            if not payload or len(payload) < 2:
                return
            if payload.decode('utf-8') == (self._LOOPBACK_DATA % self._frame_id):
                self._packet_received = True
                self._receive_lock.set()

    def execute_test(self):
        """
        Performs the loopback test.

        Returns:
            Boolean: `True` if the test succeed, `False` otherwise.
        """
        print("Executing loopback test against %s" % self._remote_device)
        # Clear vars.
        self._frame_id = 1
        self._total_loops_failed = 0
        # Store AO value.
        old_ao = _read_device_parameter_with_retries(self._local_device, ATStringCommand.AO.command)
        if old_ao is None:
            return False
        # Set AO value.
        if not _set_device_parameter_with_retries(self._local_device, ATStringCommand.AO.command, bytearray([1])):
            return False
        # Perform the loops test.
        for loop in range(self._num_loops):
            # Clear vars
            self._receive_lock.clear()
            self._packet_sent = False
            self._packet_received = False
            self._loop_failed = False
            # Add loopback callback.
            self._local_device.add_packet_received_callback(self._loopback_callback)
            try:
                # Send frame.
                self._local_device.send_packet(self._generate_loopback_packet())
                # Wait for answer.
                self._receive_lock.wait(self._loopback_timeout)
            except XBeeException as e:
                print("Could not send loopback test packet %s: %s" % (loop, str(e)))
                self._loop_failed = True
            finally:
                # Remove frame listener.
                self._local_device.del_packet_received_callback(self._loopback_callback)
            # Check if packet was sent and answer received.
            if not self._packet_sent or not self._packet_received:
                self._loop_failed = True
            # Increase failures count in case of failure.
            if self._loop_failed:
                self._total_loops_failed += 1
                # Do no continue with the test if there are already too many failures.
                if self._total_loops_failed > self._failures_allowed:
                    break
            self._frame_id += 1
            if self._frame_id > 255:
                self._frame_id = 1
        # Restore AO value.
        if not _set_device_parameter_with_retries(self._local_device, ATStringCommand.AO.command, old_ao):
            return False
        # Return test result.
        print("Loopback test result: %s loops failed out of %s" % (self._total_loops_failed, self._num_loops))
        return self._total_loops_failed <= self._failures_allowed


def _read_device_parameter_with_retries(xbee_device, parameter, retries=_PARAMETER_READ_RETRIES):
    """
    Reads the given parameter from the XBee device with the given number of retries.

    Args:
        xbee_device (:class:`.AbstractXBeeDevice`): the XBee device to read the parameter from.
        parameter (String): the parameter to read.
        retries (Integer, optional): the number of retries to perform after a :class:`.TimeoutException`

    Returns:
        Bytearray: the read parameter value, ``None`` if the parameter could not be read.
    """
    if xbee_device is None:
        return None

    while retries > 0:
        try:
            return xbee_device.get_parameter(parameter)
        except TimeoutException:
            # On timeout exceptions perform retries.
            retries -= 1
            if retries != 0:
                time.sleep(1)
        except ATCommandException as e:
            print("Could not read setting '%s': %s (%s)" % (parameter, str(e), e.status.description))
            return None
        except XBeeException as e:
            print("Could not read setting '%s': %s" % (parameter, str(e)))
            return None

    return None


def _set_device_parameter_with_retries(xbee_device, parameter, value, retries=_PARAMETER_SET_RETRIES):
    """
    Reads the given parameter from the XBee device with the given number of retries.

    Args:
        xbee_device (:class:`.AbstractXBeeDevice`): the XBee device to read the parameter from.
        parameter (String): the parameter to set.
        value (Bytearray): the parameter value.
        retries (Integer, optional): the number of retries to perform after a :class:`.TimeoutException`

    Returns:
        Boolean: ``True`` if the parameter was correctly set, ``False`` otherwise.
    """
    if xbee_device is None:
        return False

    while retries > 0:
        try:
            xbee_device.set_parameter(parameter, value)
            return True
        except TimeoutException:
            # On timeout exceptions perform retries.
            retries -= 1
            if retries != 0:
                time.sleep(1)
        except ATCommandException as e:
            print("Could not configure setting '%s': %s (%s)" % (parameter, str(e), e.status.description))
            return False
        except XBeeException as e:
            print("Could not configure setting '%s': %s" % (parameter, str(e)))
            return False

    return False


def main():
    print(" +--------------------------+")
    print(" | Continuous Transfer Test |")
    print(" +--------------------------+\n")

    device = ZigBeeDevice(PORT, BAUD_RATE, flow_control=FlowControl.HARDWARE_RTS_CTS)

    try:
        device.open()

        # Obtain the remote XBee local_xbee from the XBee network.
        xbee_network = device.get_network()
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        if remote_device is None:
            print("Could not find the remote local_xbee")
            exit(1)

        # loopback_test = _LoopbackTest(device, remote_device, loops=500)
        # if loopback_test.execute_test():
        #     print("Success")
        # else:
        #     print("Error")
        transmit_test = _TransmitTest(device, remote_device, num_packets=500)
        if transmit_test.execute_test():
            print("Success")
        else:
            print("Error")

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
