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
from digi.xbee import firmware
from digi.xbee.util import utils
from digi.xbee.exception import FirmwareUpdateException, OperationNotSupportedException, XBeeException

import logging

# TODO: Replace with the serial port where your local module is connected to. 
PORT = "/dev/ttyUSB2"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 115200
# TODO: Replace with the location of the firmware files to update.
#XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/XBP9X_9007.xml"  # SX PRO - DM
XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/XB9X_9007.xml"  # SX - DM
#XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/XB9XT_2006.xml"  # SX - XTC Hopping
#XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/XB8X_A007.xml"  # SX 868 - DM
#XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/XB3-24Z_1009-th.xml"  # XBee3 - Zigbee
BOOTLOADER_FIRMWARE_FILE = None  # Optional
XBEE_FIRMWARE_FILE = None  # Optional


def main():
    print(" +--------------------------------------------------+")
    print(" | XBee Python Library Local Firmware Update Sample |")
    print(" +--------------------------------------------------+\n")

    utils.enable_logger("digi.xbee.firmware", logging.DEBUG)

    device = XBeeDevice(PORT, BAUD_RATE)
    try:
        #device = xbee.get_device()
        device.open()
        print("Starting firmware update process...")
        device.update_firmware(XML_FIRMWARE_FILE,
                               xbee_firmware_file=XBEE_FIRMWARE_FILE,
                               bootloader_firmware_file=BOOTLOADER_FIRMWARE_FILE,
                               progress_callback=progress_callback)
        print("Firmware updated successfully!")
    except Exception as e:
        print("ERROR: %s" % str(e))
        exit(1)
    finally:
        if device is not None and device.is_open():
            device.close()


def progress_callback(task, percent):
    print("%s: %d%%" % (task, percent))


if __name__ == '__main__':
    main()
