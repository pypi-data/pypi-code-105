import pygame as pg

from PGUI.uielement import UIElement

class Slider(UIElement):
    """Creates a slider that can be dragged by the mouse.
    """
    def __init__(
            self, window,
            x: int, y: int, 
            width: int, height: int,
            min_value: int, max_value: int, default_value: int = 0,
            border_thickness: int = 3
        ) -> None:
        super().__init__(window, x, y, width, height, border_thickness)

        self.min_value = min_value
        self.max_value = max_value
        self.set_value(default_value)

        self.being_dragged = False


    def set_value(self, value) -> None:
        """Sets the position of the slider from a value within its 
        min_value and max_value.
        """
        self.pos_value = ((value-self.min_value)/self.max_value)*self.width


    def get_value(self) -> int:
        """Returns the value of the slider."""

        return min(
            int((self.pos_value/self.width)*self.max_value)+self.min_value, 
            self.max_value
        )


    def update(self) -> None:
        """Called every frame."""
        super().update()

        mouse = self.window.mouse
        mouse_x = mouse.get_pos()[0]
        bd = self.border_thickness

        ##Drag starts when element is clicked on.
        if self.clicked(0):
            self.being_dragged = True

        ##Drag continues if mouse within element x and left click held.
        self.being_dragged = (
            self.being_dragged
            and self.x+bd <= mouse_x <= self.x+self.width-bd
            and mouse.get_pressed()[0]
        )
        
        ##Update slider position if being dragged.
        if self.being_dragged:
            self.pos_value = mouse_x-self.x+bd



    def draw(self) -> None:
        """Draws the slider to the parent window."""
        super().draw()

        ##Useful little things.
        bd = self.border_thickness
        colours = self.window.colours
        screen = self.window.screen

        ##Draw slider border.
        if bd > 0:
            pg.draw.rect(
                screen, colours[3],
                [self.x, self.y, self.width, self.height]
            )

        ##Draw unfilled area of slider.
        pg.draw.rect(
            screen, colours[1],
            [self.x+bd, self.y+bd, self.width-(bd*2), self.height-(bd*2)]
        )

        ##Draw filled area of slider.
        pg.draw.rect(
            screen, colours[2],
            [self.x+bd, self.y+bd, self.pos_value-(bd*2), self.height-(bd*2)]
        )