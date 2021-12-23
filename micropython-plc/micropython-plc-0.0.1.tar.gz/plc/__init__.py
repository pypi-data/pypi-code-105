# PLC main module
# Input / Output
# Operand_AND / Operand_NAND / Operand_OR

__version__ = "0.0.1"
__license__ = "MIT"
__author__ = "Petr Kracik"

class PLCBase():
    def __init__(self, name = None):
        self.__value = None
        self._name = name or type(self).__name__
        self._on_change_events = []


    @property
    def name(self):
        return self._name


    @property
    def output(self):
        return self._value


    @property
    def _value(self):
        return self.__value


    @_value.setter
    def _value(self, value):
        if value is None:
            self.__value = None
            return

        tmp = bool(value)
        if tmp == self.__value:
            return

        direction = PLCInterrupt.RISING if tmp else PLCInterrupt.FALLING
        self.__value = tmp
        self._on_change_event(tmp, direction)


    def _on_change_event(self, value, direction):
        print("PLCBase: ev_change: {}: {}".format(self.name, value))
        for f in self._on_change_events:
            f(self, value, direction)


    def add_event_on_change(self, func):
        self._on_change_events.append(func)


    def remove_event_on_change(self, func):
        if func in self._on_change_events:
            del self._on_change_events[func]


class PLCException(Exception):
    pass


class PLCInterrupt():
    FALLING = 0
    RISING = 1


class PLCOverride(PLCBase):
    def __init__(self, input, enabled=False, value=False):
        self._input = input
        self._enabled = enabled
        self._value = value


    @property
    def enabled(self):
        return self._enabled


    @enabled.setter
    def enabled(self, en):
        self._enabled = en


    @property
    def output(self):
        if self._enabled:
            return self._value
        else:
            return self._input.output


    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, value):
        self._value = value
