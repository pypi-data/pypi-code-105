from plc import PLCBase, PLCInterrupt


class PLCInput(PLCBase):
    def __init__(self, name=None):
        super().__init__(name)
