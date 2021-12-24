import pygame as pg

from PGUI.uielement import UIElement

class RawText(UIElement):
    """Displays text in a given font and size.
    Note: Does not account for width or height constraints.
    
    Parameters
    ----------
    - All `UI_Element` parameters minus width and height.
    - `text: str` - The text to be displayed.
    - `font: tuple(font_path: str, font_size: int)` - The font in which to
      display the text.
    - `colour: tuple or int` - The colour to draw the text in.

    Methods
    -------
    - All `UI_Element` methods.
    - `get_size() -> tuple(int, int)` - Get size of the text.
    """
    def __init__(
            self, window,
            x: int, y: int, 
            text: str, font, colour,
        ) -> None:

        super().__init__(window, x, y, 0, 0)

        self.text = text
        self.font: pg.font.Font = pg.font.Font(*font)

        ##If colour is int, use it as index of window's colours.
        if isinstance(colour, int):
            self.colour = self.window.colours[colour]
            self.colour_index = colour
        ##If colour is list or tuple, use values to make colour.
        elif isinstance(colour, (tuple, list)):
            self.colour = colour
            self.colour_index = None
        else:
            raise TypeError("Invalid colour argument.")


    def draw(self) -> None:
        """Draw text to window."""
        text = self.font.render(self.text, False, self.colour)
        self.window.screen.blit(text, (self.x, self.y))


    def get_size(self) -> tuple:
        """Return size of text."""
        return self.font.size(self.text)


    def update_colours(self) -> None:
        if self.colour_index:
            self.colour = self.window.colours[self.colour_index]






class WrappedText(RawText):
    """Wraps text to fit within width and height constraints.
    """
    def __init__(
            self, window,
            x: int, y: int, 
            width: int, height: int,
            text: str, font, colour: tuple, centred: bool = False,
        ) -> None:
        super().__init__(window, x, y, text, font, colour)

        self.width = width
        self.height = height

        self.font = font[0]
        self.font_size = font[1]
        self.pg_font = pg.font.Font(*font)
        self.centred = centred
        self.text_width = 0
        self.text_height = 0

        ##Any text that doesn't fit
        self.cut_text = ""


    def draw(self) -> None:
        """Draws the text wrapped in a box."""
        ##str() called so that changes to text don't change self.text
        text = str(self.text)

        ##Get the height of the tallest letter in the font
        font_height = self.pg_font.size("T")[1]
        line_spacing = 3
        
        display = []
        i = 0
        y = int(self.y)
        width = 0
        new_line = False

        while text:

            new_line = False

            ##Stops loop if out of y space.
            if y + font_height > y + self.height:
                break

            ##Increments i until it runs out of x space.
            while self.pg_font.size(text[:i])[0] < self.width and i < len(text):
                i += 1
                if text[i-1] == "\n":
                    new_line = True
                    break

            ##Finds the last space if there is still text to display.
            if i < len(text) and new_line == False:
                i = text.rfind(" ", 0, i) + 1

            if i != 0:
                if (text[:i][-1] == " " or text[:i][-1] == "\n"):
                    display.append(
                        self.pg_font.render(text[:i-1], False, self.colour)
                    )
                else:
                    display.append(
                        self.pg_font.render(text[:i], False, self.colour)
                    )

            new_line = False
            text = text[i:]
            if i == 0:
                break

        total_height = len(display) * (font_height + line_spacing)

        for image in display:
            if self.centred:
                self.window.screen.blit(
                    image, 
                    (
                        self.x+(self.width/2)-image.get_rect().width/2, 
                        y+(self.height/2)-(total_height/2))
                    )
            else:
                width = max(width, image.get_rect()[2])
                self.window.screen.blit(image, (self.x, y))
                
            y += font_height+line_spacing

        ##Return actual width and height of text
        self.text_height = y - self.y
        self.text_width = width

        if text:
            self.cut_text = text
        else:
            self.cut_text = ""