import pygame as pg

from PGUI.uielement import UIElement

class Panel(UIElement):

    def draw(self):
        super().draw()
        bd = self.border_thickness
        ##Border rect.
        pg.draw.rect(
            self.window.screen, self.window.colours[3], 
            [self.x, self.y, self.width, self.height]
        )
        ##Colour rect.
        pg.draw.rect(
            self.window.screen, self.window.colours[0], 
            [self.x+bd, self.y+bd, self.width-(bd*2), self.height-(bd*2)]
        )