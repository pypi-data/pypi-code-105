from typing import List
import pygame as pg

class UIElement:
    """All UI elements must inherit from this class. Gives basic methods and
        attributes for UI use.
    """
    def __init__(
                self, 
                window,
                x: int, y: int, 
                width: int, height: int, 
                border_thickness: int = 3
            ) -> None:

        ##Drawing details.
        from PGUI.window import Window
        self.window: Window = window
        "The parent window of the UI element."
        self.x = x
        "The X screen position of the element."
        self.y = y
        "The Y screen position of the element."
        self.width = width
        "The width of the element in pixels."
        self.height = height
        "The height of the element in pixels."
        self.border_thickness = border_thickness
        "How thick the border of the element should be."
        self.drawing = True
        """Controls whether or not the element is drawn."""

        ##Tooltip stuff.
        self.use_tooltip = False
        """Whether to display a tooltip for this element or not."""
        self.tooltip_title = ""
        """The title for the tooltip class to draw."""
        self.tooltip_text = ""
        """The text for the tooltip class to display."""

        ##Child stuff.
        self.is_child = False
        """True if element is a child of another element."""
        self.children: List[UIElement] = []
        """Child elements of element."""

        ##If parent is another UI element, add self as child and get window.
        if isinstance(self.window, UIElement):
            self.is_child = True
            self.window.add_child(self)
            self.window = self.window.window
            return
        else:
            ##Add element to window.
            self.window.add_ui_element(self)



    #region mouse
    def mouse_on_element(self, mouse) -> bool:
        """Returns true if mouse is within element bounding box"""
        bd = self.border_thickness
        return (
            (self.x + bd <= mouse[0] <= self.x + self.width - (bd*2)) and
            (self.y + bd <= mouse[1] <= self.y + self.height - (bd*2))
        ) 


    def on_click(self) -> None:
        """Called when element is clicked."""
        ##Does nothing by default.
        pass


    def clicked(self, button=0) -> bool:
        return (self.mouse_on_element(self.window.mouse.get_pos()) 
                and any([event.type == pg.MOUSEBUTTONDOWN for event in self.window.events])
                and self.window.mouse.get_pressed()[button]
            )


    def mouse_held(self, button=0) -> bool:
        """Returns true if element is clicked and held."""
        return (self.mouse_on_element(self.window.mouse.get_pos()) 
                and self.window.mouse.get_pressed()[button])
    #endregion



    def add_child(self, child):
        """
        Add a child UI Element to the element.
        Note: if this is not called to add a child element it may break
        automated element spacing within windows."""
        self.children.append(child)
        child.is_child = True


    def update(self) -> None:
        """Called once every frame."""
        if not self.window.running:
            return

        if self.clicked():
            self.on_click()

        for child in self.children:
            child.update()


    def draw(self) -> None:
        """Called once every frame and draws the element."""
        if not self.drawing:
            return

        for child in self.children:
            child.draw()


    def update_colours(self) -> None:
        if self.children:
            for child in self.children:
                child.update_colours()


    def set_x(self, new_x):
        self.x = new_x
        if self.children:
            for child in self.children:
                child.set_x(new_x)


    def set_y(self, new_y):
        self.y = new_y
        if self.children:
            for child in self.children:
                child.set_y(new_y)


    def set_width(self, new_width):
        self.width = new_width
        if self.children:
            for child in self.children:
                child.set_width(new_width)
    

    def set_height(self, new_height):
        self.height = new_height
        if self.children:
            for child in self.children:
                child.set_height(new_height)