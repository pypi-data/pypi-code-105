import pygame as pg

from PGUI.UIElements.button import Button

class ToggleButton(Button):
    def __init__(
            self, window,
            x: int, y: int, 
            width: int, height: int, 
            text: str = "", text_size: int = 10, 
            action=None, arguments: tuple = None, 
            border_thickness: int = 3
        ) -> None:
        super().__init__(
            window, 
            x, y, 
            width, height, 
            text=text, text_size=text_size, 
            action=action, arguments=arguments, 
            border_thickness=border_thickness
        )
        self.active = False

    def on_click(self) -> None:
        super().on_click()
        self.active = not self.active

    def draw(self):
        ##If hovering or active, use colour 3
        ##If clicked, use colour 4
        ##Else use colour 2
        if self.mouse_on_element(self.window.mouse.get_pos()):
            if (self.window.mouse.get_pressed()[0]):
                button_colour = self.window.colours[3]
            else:
                button_colour = self.window.colours[2]
        else:
            button_colour = self.window.colours[1]

        if self.active:
            button_colour = self.window.colours[2]

        ##Draw border rect
        bd = self.border_thickness
        if bd > 0:
            pg.draw.rect(
                self.window.screen, self.window.colours[3],
                [self.x, self.y, self.width, self.height]
            )
        
        ##Draw button
        pg.draw.rect(
            self.window.screen, button_colour,
            [self.x+bd, self.y+bd, self.width-(bd*2), self.height-(bd*2)]
        )

        self.text.draw()

        ##Reduce text size if any is cut off
        if self.text.cut_text != "":
            self.text.font_size -= 1
            self.text.pg_font = pg.font.Font(
                self.text.font, self.text.font_size
            )