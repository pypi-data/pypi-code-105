from typing import Tuple
import pygame as pg

from PGUI.uielement import UIElement
from PGUI.UIElements.text import WrappedText

class Button(UIElement):
    """
    Creates a button that the user can press to call an action.

    Parameters
    ----------
    - All `UIElement` parameters.
    - `text: str` - The text to display on the button.
    - `text_size: int` - The size (in pixels) to display the text.
    - `action: method` - The method to call when the button is clicked.
    - `arguments: tuple` - Arguments to pass to the method or function.

    Methods
    -------
    - All `UIElement` methods.
    - `update() -> None` - Called by the parent window every frame to update 
      the button.
    - `draw() -> None` - Called by the parent every frame to draw the button.
    """

    def __init__(
            self, window,
            x: int, y: int, 
            width: int, height: int,
            text: str = "", text_size: int = 10, 
            action = None, arguments: tuple = None,
            border_thickness: int = 3
        ) -> None:

        ##Initialise the UIElement.
        super().__init__(window, x, y, width, height, border_thickness)

        self.text = WrappedText(
            self,
            self.x+5, self.y+5,
            self.width-10, self.height-10,
            text, (self.window.font, text_size), 
            self.window.colours[0],
            True
        )
        """Text to display on button."""

        self.action = action
        """Method or function for the button to call on click."""
        self.arguments = arguments
        """Arguments to be passed to button function or method."""


    def on_click(self) -> None:
        """Calls the button's argument(s)."""
        if self.action != None:
            if self.arguments == None: 
                self.action()
            elif isinstance(self.arguments, Tuple):
                self.action(*self.arguments)
            else:
                self.action(self.arguments)


    def draw(self):
        """Draw the button to the screen."""

        mouse = self.window.mouse
        ##If hovering, use colour 3.
        if self.mouse_on_element(mouse.get_pos()):
            ##If clicked, use colour 3.
            colour_index = 3 if mouse.get_pressed()[0] else 2
        else:
            ##If not hovering use colour 2.
            colour_index = 1

        button_colour = self.window.colours[colour_index]

        ##Draw border rect.
        bd = self.border_thickness
        if bd > 0:
            pg.draw.rect(
                self.window.screen, 
                self.window.colours[3],
                [self.x, self.y, self.width, self.height]
            )

        ##Draw button.
        pg.draw.rect(
            self.window.screen, 
            button_colour,
            [self.x+bd, self.y+bd, self.width-(bd*2), self.height-(bd*2)]
        )

        self.text.draw()

        ##Reduce text size if any is cut off
        if self.text.cut_text != "":
            self.text.font_size -= 1
            self.text.pg_font = pg.font.Font(self.text.font, self.text.font_size)


    def update_colours(self) -> None:
        super().update_colours()
        self.text.colour = self.window.colours[0]