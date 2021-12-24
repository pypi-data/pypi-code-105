import pygame as pg
import string

from pygame.constants import KEYDOWN

from PGUI.UIElements.togglebutton import ToggleButton

class InputField(ToggleButton):
    #region perameters
    def __init__(
            self, window,
            x: int, y: int, 
            width: int, height: int, 
            text: str = "", 
            numbers_only: bool = False, 
            censored: bool = False,
            text_size: int = 10, 
            border_thickness: int = 3,
        ):
        super().__init__(
            window,
            x, y, width, height, 
            text=text, 
            text_size=text_size, 
            action=None, arguments=None, 
            border_thickness=border_thickness, 
        )
    #endregion

        self.active = False
        self.text_value = text
        self.censored = censored

        ##Set allowed characters based on numbers_only.
        if numbers_only:
            self.ALLOWED_CHARS = string.digits
        else:
            self.ALLOWED_CHARS = (
                string.digits
                + string.ascii_letters 
                + string.punctuation
                ##string.whitespace isn't used because it allows return.
                + " "
            )

    def update(self):
        super().update()
        ##Show visible text as "*" symbols if input box is censored.
        if self.censored:
            self.text.text = "*" * len(self.text_value)
        else:
            self.text.text = self.text_value

        ##If mouse is clicked, set active if it is on element.
        if self.window.mouse.get_pressed()[0]:
            self.active = self.mouse_on_element(self.window.mouse.get_pos())

        ##Check for key input when active.
        if self.active:
            key_events = [i for i in self.window.events if i.type == pg.KEYDOWN]
            for key_down in key_events:
                if key_down.key == pg.K_BACKSPACE:
                    self.text_value = self.text_value[:-1]
                    continue
                elif key_down.unicode in self.ALLOWED_CHARS:
                    self.text_value += key_down.unicode

    def get_value(self):
        """Return input field value."""
        return self.text_value