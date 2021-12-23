from plc import PLCBase


class PLCOperand(PLCBase):
    def __init__(self, name=None):
        super().__init__(name)


    def __on_input_change(self, input, value, dir):
        self._value = self.output
