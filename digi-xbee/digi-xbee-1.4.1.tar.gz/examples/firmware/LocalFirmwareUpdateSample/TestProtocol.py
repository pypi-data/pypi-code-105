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

from digi.xbee.devices import XBeeDevice, DigiMeshDevice, ZigBeeDevice
from digi.xbee.exception import FirmwareUpdateException, OperationNotSupportedException, XBeeException
from digi.xbee.util import utils

# TODO: Replace with the serial port where your local module is connected to.
PORT = "/dev/ttyUSB2"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 115200
# TODO: Replace with the location of the firmware files to update.
#XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/XB3-24DM_3004-th.xml"
XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/XB3-24Z_1008-th.xml"
#XML_FIRMWARE_FILE = "/home/descalon/test_xbee_firmware/radio_fw/XB3-24Z_1009-th.xml"
BOOTLOADER_FIRMWARE_FILE = None  # Optional
XBEE_FIRMWARE_FILE = None  # Optional


def main():
    print(" +--------------------------------------------------+")
    print(" | XBee Python Library Local Firmware Update Sample |")
    print(" +--------------------------------------------------+\n")

    device = DigiMeshDevice(PORT, BAUD_RATE)

    try:
        device.open()
        print("Protocol: %s" % device.get_protocol().name)
        print("Firmware version: %s" % hex(utils.bytes_to_int(device.get_firmware_version())))
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
