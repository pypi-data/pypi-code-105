from plc.elements import PLCElement


class PLCElementRS(PLCElement):
    def __init__(self, set_element=None, reset_element=None, name=None, value=None):
        super().__init__(value, name)
        self.set = set_element
        self.reset = reset_element


    @property
    def set(self):
        return self._set_element


    @set.setter
    def set(self, element):
        if not element:
            return

        element.add_event_on_change(self.__on_input_change)
        self._set_element = element


    @property
    def reset(self):
        return self._reset_element


    @reset.setter
    def reset(self, element):
        if not element:
            return

        element.add_event_on_change(self.__on_input_change)
        self._reset_element = element


    @property
    def output(self):
        s = self._set_element.output
        r = self._reset_element.output
        if r == s:
            return self._value or s

        if s:
            self._value = True

        if r:
            self._value = False

        return self._value
