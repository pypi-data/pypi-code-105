# Copyright 2019, Digi International Inc.
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

from digi.xbee.devices import XBeeDevice
from digi.xbee.exception import FirmwareUpdateException, OperationNotSupportedException, XBeeException
from digi.xbee.util import utils

import logging

# TODO: Replace with the serial port where your local module is connected to.
PORT = "/dev/ttyUSB2"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 115200
# TODO: Replace with the Node ID (NI) of the remote module to update.
REMOTE_NODE_ID = "DAVID_ROUTER_3"
# TODO: Replace with the location of the firmware files to update.
#XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/XB3-24Z_1005.xml"
XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/XB3-24Z_1008.xml"
#XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/XB3-24Z_100A.xml"
#XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/XB3-24Z_1009-th.xml"
#XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/XB3-24Z_1008-th.xml"
#XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/XB9X_9007.xml"  # 900 MHz
#XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/XB8X_A007.xml"  # 868 MHz
#XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/xbp24-s2c_4061.xml"  # S2C ZigBee
#XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/xbp24c-dm-smt_9002.xml"  # S2C DigiMesh HV 0x30
#XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/xb24c-dm-smt_9002.xml"  # S2C DigiMesh HV 0x22
#XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/xbp24c-smt_2003.xml"  # S2C 802.15.4
OTA_FIRMWARE_FILE = None  # Optional
OTB_FIRMWARE_FILE = None  # Optional


def main():
    print(" +---------------------------------------------------+")
    print(" | XBee Python Library Remote Firmware Update Sample |")
    print(" +---------------------------------------------------+\n")

    utils.enable_logger("digi.xbee.firmware", logging.DEBUG)

    device = XBeeDevice(PORT, BAUD_RATE)
    try:
        device.open()
        # Obtain the remote XBee device from the XBee network.
        xbee_network = device.get_network()
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        if remote_device is None:
            print("Could not find the remote device")
            exit(1)
        print("Starting firmware update process...")
        remote_device.update_firmware(XML_FIRMWARE_FILE,
                                      xbee_firmware_file=OTA_FIRMWARE_FILE,
                                      bootloader_firmware_file=OTB_FIRMWARE_FILE,
                                      progress_callback=progress_callback)
        print("Firmware updated successfully!")
    except (XBeeException, FirmwareUpdateException, OperationNotSupportedException) as e:
        print("ERROR: %s" % str(e))
        exit(1)
    finally:
        if device is not None and device.is_open():
            device.close()


def progress_callback(task, percent):
    print("%s: %d%%" % (task, percent))


if __name__ == '__main__':
    main()
