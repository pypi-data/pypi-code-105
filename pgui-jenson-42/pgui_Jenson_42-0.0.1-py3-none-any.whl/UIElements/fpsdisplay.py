from PGUI.UIElements.text import RawText

class FPSDisplay(RawText):
    def __init__(
            self, window, 
            x: int, y: int, 
            font, colour: int, 
            clock,
        ) -> None:
        super().__init__(
            window, 
            x, y,
            "", font, 
            colour,
        )
        self.clock = clock

    def update(self) -> None:
        fps = round(self.clock.get_fps())
        self.text = f"FPS: {fps}"