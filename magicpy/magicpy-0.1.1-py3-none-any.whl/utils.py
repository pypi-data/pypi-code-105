import serial.tools.list_ports
ports = serial.tools.list_ports.comports()


def list_ports():
    """
    Prints available serial ports on the machine.

    Returns
    -------
    list : List of available ports

    """
    ports = []
    for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))
            port.append(port)
    return ports