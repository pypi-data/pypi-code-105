from PGUI.UIElements.panel import Panel
from PGUI.UIElements.text import WrappedText

class TitleScreen(Panel):
    def __init__(
            self, window,
            x: int, y: int, 
            width: int, height: int, 
            text, font,
            border_thickness: int = 3
        ) -> None:
        super().__init__(
            window, 
            x, y, 
            width, height, 
            border_thickness=border_thickness
        )
        self.text = text
        self.font = font
    
    def draw(self) -> None:
        super().draw()
        WrappedText(
            self.x, self.y, self.width, self.height, self.text, self.font,
            self.window.colours[3], window=self.window, centred=True
        ).draw()