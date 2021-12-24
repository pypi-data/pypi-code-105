import pygame as pg

from PGUI.UIElements.button import Button

class DropDown(Button):
    def __init__(
        self, window, 
        x: int, y: int, 
        width: int, height: int, 
        text: str, items: tuple, dropdown_action=None,
        default_item = None,
        text_size=10, border_thickness: int = 3
    ) -> None:
        super().__init__(
            window, x, y, width, height, text, text_size,
            border_thickness=border_thickness
        )
        self.items = items
        self.buttons = []
        self.selected_item = None
        self.dropdown_text = text
        self.dropdown_action = dropdown_action
        self.open = False
        self.text_size = text_size
        i = self.y
        for item in self.items:
            button = Button(
                    self,
                    self.x+2, self.height+i+2, self.width-4, self.height-4, 
                    str(item), text_size, self.update_selected, (item), 
                    1
                )
            self.buttons.append(button)
            i += self.height
        
        self.update_selected(default_item)

    def update(self) -> None:
        super().update()
        if self.clicked():
            self.open = not self.open
        if self.open:
            for button in self.buttons:
                button.update()

    def draw(self) -> None:
        super().draw()
        if self.open:
            for button in self.buttons:
                button.draw()

    def update_selected(self, item) -> None:
        self.selected_item = item
        self.open = False
        self.text.text = f"{self.dropdown_text}: {item}"
        if self.dropdown_action != None:
            self.dropdown_action(item)