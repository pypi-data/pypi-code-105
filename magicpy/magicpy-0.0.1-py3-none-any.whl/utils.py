import serial.tools.list_ports
ports = serial.tools.list_ports.comports()


def list_ports():
    """
    Small function to list available serial ports on current machine.

    """
    for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))