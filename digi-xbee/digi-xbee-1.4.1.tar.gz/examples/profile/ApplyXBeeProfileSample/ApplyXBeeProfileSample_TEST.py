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
from digi.xbee.util import utils

import logging

PROFILE_PATH = "/home/descalon/test_xbee_firmware/DAVID_SX_DM_1.xpro"
PORT = "/dev/ttyUSB2"
BAUD_RATE = 115200


def main():
    print(" +----------------------------------------------+")
    print(" | XBee Python Library Read XBee Profile Sample |")
    print(" +----------------------------------------------+\n")

    utils.enable_logger("digi.xbee.firmware", logging.DEBUG)

    device = XBeeDevice(PORT, BAUD_RATE)
    try:
        device.open()
        print("Updating profile '%s'...\n" % PROFILE_PATH)
        device.apply_profile(PROFILE_PATH, progress_callback=progress_callback)
        print("\nProfile updated successfully!")
    except Exception as e:
        print(str(e))
        exit(1)
    finally:
        if device.is_open():
            device.close()


def progress_callback(task, percent):
    if percent is not None:
        print("%s: %d%%" % (task, percent))
    else:
        print("%s" % task)


if __name__ == '__main__':
    main()
