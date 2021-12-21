"""
Python provisioning of IoT kits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

iotprovision is a command-line utility for provisioning Microchip AVR-IoT
and PIC-IoT kits for use with various cloud providers.

It is used as a CLI.

Type iotprovision --help to get help.

Dependencies
~~~~~~~~~~~~
iotprovision depends on pytrustplatform, pyawsutils and pyazureutils.
iotprovision depends on pykitcommander to manage Microchip IoT kit firmware
and connection.
iotprovision depends on pyedbglib for its transport protocol.
pyedbglib requires a USB transport library like libusb.
See pyedbglib package for more information: https://pypi.org/project/pyedbglib/
"""

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
