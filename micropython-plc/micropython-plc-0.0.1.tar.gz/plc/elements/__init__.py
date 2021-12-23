from plc import PLCBase


class PLCElement(PLCBase):
    def __init__(self, value=None, name=None):
        super().__init__(name)
        self._value = value

    def __on_input_change(self, input, value, dir):
        self._value = self.output
