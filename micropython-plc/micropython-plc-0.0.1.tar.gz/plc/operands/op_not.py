from plc.operands import PLCOperand


class PLCOperandNOT(PLCOperand):
    def __init__(self, input, name=None):
        super().__init__(name)
        input.add_event_on_change(self.__on_input_change)
        self._input = input


    @property
    def output(self):
        return not self._input.output
