from plc.operands import PLCOperand


class PLCOperandAND(PLCOperand):
    def __init__(self, inputs=None, name=None):
        super().__init__(name)
        self._inputs = inputs or list()


    def add_input(self, input):
        input.add_event_on_change(self.__on_input_change)
        self._inputs.append(input)
        self._value = self.output


    def remove_input(self, input):
        if input not in self._inputs:
            return

        self._value = self.output


    @property
    def output(self):
        for i in self._inputs:
            val = i.output
            if not val:
                return False

        return True


class PLCOperandNAND(PLCOperandAND):
    # Because micropython does not allow calling super().output property
    # This ugly hack must be done
    @property
    def output(self):
        for i in self._inputs:
            val = i.output
            if not val:
                return True

        return False
