from plc.outputs import PLCOutput

class PLCOutputVirtual(PLCOutput):
    def __init__(self, input, name=None):
        super().__init__(input, name)
        self.add_event_on_change(self._on_change)


    def _on_change(self, obj, value, direction):
        print("Virtual output \"{}\" changed to {}".format(self.name, value))
