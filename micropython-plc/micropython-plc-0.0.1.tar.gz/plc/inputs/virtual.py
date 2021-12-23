from plc.inputs import PLCInput

class PLCInputVirtual(PLCInput):
    def __init__(self, value=0, name=None):
        super().__init__(name)
        self._value = value


    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, value):
        self._value = value
