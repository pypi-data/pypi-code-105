import pygame as pg 

from PGUI.uielement import UIElement
from PGUI.UIElements.text import RawText, WrappedText

class Tooltip(UIElement):
    """Adds a tooltip that follows the mouse and displays information about
    any UI elements the user hovers over. UIElement.use_tooltip must be True
    to use this feature and it is False by default.
    - UIElement.tooltip_title sets the title for the tooltip
    - UIElement.tooltip_text sets the body text for the tooltip

    The tooltip will automatically size itself to fit the text it's 
    displaying.
    """

    def __init__(
            self, window,
            border_thickness: int = 1,
        ) -> None:
        super().__init__(window, 0, 0, 200, 50, border_thickness)
        self.drawing = False

        self.title = RawText(
            self,
            0, 0, "", 
            (window.font, 15), 2
        )

        self.text = WrappedText(
            self,
            0, 0, 400, 10000, "", 
            (window.font, 10), 2
        )

    def get_element_hovering(self) -> UIElement:
        """Get highest-layer element mouse is currently hovering over with
        use_tooltip enabled."""
        elements_hovering = [
            element for element in self.window.ui_elements
            if element.mouse_on_element(self.window.mouse.get_pos())
            and element.use_tooltip
        ]
        if elements_hovering == []:
            return None
        else:
            ##Return last element in list (highest render priority)
            return elements_hovering[-0]

    def update(self) -> None:
        """Update position to mouse position and set title and text to that of
        the UIElement of the highest position in window.ui_elements."""
        mouse_pos = self.window.mouse.get_pos()

        ##Get highest element.
        element = self.get_element_hovering()
        ##Return if not hovering over tooltip-enabled element.
        if element == None:
            self.drawing = False
            return

        self.drawing = True
        self.title.text = element.tooltip_title

        ##Fit tooltip to title size if body text not present.
        if element.tooltip_text == "":
            self.tooltip_text = ""
            self.height = self.title.get_size()[1] + 4
            self.width = self.title.get_size()[0]
        else:
            ##set width to widest text.
            self.width = (
                max(
                    self.title.get_size()[0],
                    self.text.text_width
                ) + 2
            )
            self.text.text = element.tooltip_text
            ##Set height to sum of title and text height.
            self.height = (
                self.title.get_size()[1] 
                + self.text.text_height 
                + 8
                )

        ##Put tooltip left of mouse if rendering it right would go off-screen.
        if self.width + mouse_pos[0] > self.window.screen_size[0]:
            self.x = mouse_pos[0]-self.width-5
        else:
            self.x = mouse_pos[0]

        ##Put tooltip above mouse if rendering it below would go off-screen.
        if self.height + mouse_pos[1] > self.window.screen_size[1]:
            self.y = mouse_pos[1]-self.height-5
        else:
            self.y = mouse_pos[1]+5

        self.title.x, self.title.y = self.x+2, self.y+2
        self.text.x, self.text.y = self.x+2, self.y+22

    def draw(self) -> None:
        """Draw tooltip to parent window."""
        if not self.drawing:
            return None

        super().draw()
        draw = pg.draw
        window = self.window
        bd = self.border_thickness

        ##Draw border rect.
        draw.rect(
            window.screen, window.colours[3], 
            [self.x-bd, self.y-bd, self.width+2*bd, self.height+2*bd]
        )
        ##Draw inner rect.
        draw.rect(
            window.screen, window.colours[0], 
            [self.x, self.y, self.width, self.height]
        )
        ##Draw text
        self.title.draw()
        self.text.draw()