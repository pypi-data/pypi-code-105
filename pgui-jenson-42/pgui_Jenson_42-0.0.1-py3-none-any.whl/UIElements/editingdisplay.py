from PGUI.spacing import space_elements
import PGUI.UIElements as elements

class EditingDisplay(elements.Panel):
    def __init__(
            self, window, 
            x: int, y: int, 
            width: int, height: int, 
            border_thickness: int = 3
        ) -> None:
        super().__init__(
            window, 
            x, y, width, height, 
            border_thickness=border_thickness
        )

        elements.RawText(
            self,
            605, 175,
            "Editing Map:",
            (self.window.font, 10), 3
        )

        self.map_name_text = elements.RawText(
            self,
            605, 190,
            "",
            (self.window.font, 10), 2
        )

        elements.RawText(
            self,
            605, 205,
            "Selected Tile:",
            (self.window.font, 10), 3
        )

        self.tile_name_text = elements.RawText(
            self,
            605, 220,
            "",
            (self.window.font, 10), 2
        )

        elements.RawText(
            self,
            605, 235,
            "Description:",
            (self.window.font, 10), 3
        )

        self.tile_desc_text = elements.WrappedText(
            self,
            605, 250,
            165, 200,
            "",
            (self.window.font, 10), 2, False
        )

        y_positions, heights = space_elements(
            [1, 1, 1, 1, 1, 10],
            self.height,
            5, 5, self.y
        )

        for index, element in enumerate(self.children):
            element.set_y(y_positions[index])
            element.set_height(heights[index])

    def update(self) -> None:
        super().update()
        self.map_name_text.text = self.window.editor_grid.map_name

        tile = self.window.parent.selected_tile
        if tile:
            self.tile_name_text.text = tile.tile_name
            self.tile_desc_text.text = tile.tile_description


    def draw(self):
        super().draw()
        for child in self.children:
            child.draw()
