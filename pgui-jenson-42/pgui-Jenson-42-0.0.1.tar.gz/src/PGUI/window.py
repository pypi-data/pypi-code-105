"""Adds a window, innit?"""

import pygame as pg
from PGUI.uielement import UIElement

class Window:
    """Creates a window using pygame.
    - UIElements can be added to the window, and their update() and draw()
      methods will be called every frame.
    """
    #region meta
    def __init_subclass__(cls, window_id: str, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        ##Each subclass of Window must have a window_id.
        cls.window_id = window_id

    def __str__(self) -> str:
        screen_size = f"(X){self.screen_size[0]}px (Y){self.screen_size[1]}px"
        return (f"Window '{self.window_id}': title = {self.title}, size = {screen_size}")
    #endregion

    def __init__(
            self, 
            parent, 
            title: str, 
            width: int, 
            height: int,
        ) -> None:

        ##Display stuff.
        self.screen_size: tuple = (width, height)
        """The width and height of the screen in pixels."""
        self.title: str = title
        """The title to be displayed at the top of the window."""
        from PGUI.program import Program
        self.parent: Program = parent
        """Window's parent program."""
        self.colours = self.parent.colours
        """List of colours used by the window."""

        ##Pygame stuff.
        self.running: bool = False
        self.fps: int = 60
        """Number of frames per second to draw the window at."""
        self.clock = pg.time.Clock()
        """Pygame clock to control FPS."""
        self.mouse = pg.mouse
        """Reference to the pygame mouse."""
        self.events = []
        """List of pygame events, updated every frame."""

        ##Font.
        pg.font.init()
        self.font: str = "Assets/Fonts/GravityRegular5.ttf"
        """The text font to be used throughout the window."""

        ##List of UI elements.
        self.ui_elements: list[UIElement] = []
        """List of UI elements that the window draws and updates every 
        frame."""

        ##Add self to controller.
        self.parent.add_window(self, self.window_id)


    def add_ui_element(self, ui_element: UIElement) -> None:
        """Adds a UI element to the window."""
        self.ui_elements.append(ui_element)
        ui_element.window = self


    def add_ui_elements(self, ui_elements: list) -> None:
        """Adds multiple UI elements to the window."""
        for ui_element in ui_elements:
            self.ui_elements.append(ui_element)
            ui_element.window = self


    def remove_ui_element(self, ui_element: UIElement) -> None:
        """Removes a UI element from the window."""
        self.ui_elements.remove(ui_element)


    def update(self) -> None:
        """Called every frame"""
        ##Get events. 
        ##In try except because program crashes on close otherwise.
        try:
            self.events = pg.event.get()
        except pg.error:
            self.end()

        ##Close window if close button clicked or parent stops running.
        if (
            any(event.type == pg.QUIT for event in self.events) 
            or not self.parent.running
           ):
            self.end()
            return
        
        ##Update the window's UI elements.
        for ui_element in self.ui_elements:
            ui_element.update()


    def draw(self) -> None:
        """Called every frame and draws the window."""
        if not self.parent.running:
            return

        ##Fills the screen. Drawing code run before this will not display.
        self.screen.fill(self.colours[0])

        ##Draws each of the UI elements in the window.
        for ui_element in self.ui_elements:
            ui_element.draw()

        ##Displays what's been drawn.
        pg.display.flip()

    def run(self) -> None:
        """
        Starts the window running. This is called once when the window is
        first opened."""
        self.running = True
        self.setup()

        while self.running:
            self._run()
            self.clock.tick(self.parent.fps)

    def setup(self) -> None:
        """
        Sets the window up. If this isn't called before the window is
        opened it will retain the old window's size and title."""
        self.screen = pg.display.set_mode(self.screen_size)
        pg.display.set_caption(self.title)
        
    def _run(self) -> None:
        """
        Runs the window. This function contains anything that needs to
        happen every frame."""     
        self.update()
        self.draw()


    def end(self) -> None:
        """
        Closes the window. Any code that needs to happen before the window
        closes goes here."""
        self.running = False


    def open_window(self, window_id):
        """
        Opens another window and then runs own setup method. This prevents
        window A from retaining window B's size when B is closed."""
        window = self.parent.get_window(window_id)
        window.run()
        self.setup()


    def update_colours(self, colours: list):
        self.colours = colours
        for element in self.ui_elements:
            element.update_colours()
