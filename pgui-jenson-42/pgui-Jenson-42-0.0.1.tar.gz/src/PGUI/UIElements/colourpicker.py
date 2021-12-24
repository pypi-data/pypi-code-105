import pygame as pg
import os.path
import json

from PGUI.spacing import space_elements
from PGUI.uielement import UIElement
from PGUI.UIElements.slider import Slider
from PGUI.UIElements.button import Button
from PGUI.UIElements.text import RawText
from PGUI.UIElements.panel import Panel

class ColourPicker(UIElement):
    """Creates 3 sliders for each colour in the parent window palette.
    - Users can change each RGB value and see the colours update in the
      preview boxes next to them in real time.

    Also adds 3 buttons:
    - "Apply" button will save the selected colours to the parent window and
      it's parent controller (if present).
    - "Reset" button sets the sliders back to their last saved state.
    - "Defaults" button sets the values back to their hard-coded defaults.
    """
    def __init__(
            self, window,
            x: int, y: int, 
            width: int, height: int,
            border_thickness: int = 3
        ) -> None:
        super().__init__(window, x, y, width, height, border_thickness)

        self.colours = list(self.window.colours)
        self.palette_directory = "Assets/palettes/"
        self.palettes = self.load_palettes()
        self.palette_index = -1
        self.ugh = False

        ##Child UI elements
        self.colour_sliders = []
        self.channel_text = []
        self.colour_text = []
        self.buttons = []

        ##Background panel
        Panel(
            self,
            x, y, 
            width, height-border_thickness, 
            border_thickness
        )

        element_ratios = []
        for colour in self.window.colours:
            element_ratios.append(1)
            for channel in colour:
                element_ratios.append(1)
        ##Buttons are twice the height of each slider.
        element_ratios.append(2)

        y_positions, heights = space_elements(
            elements=element_ratios,
            size=self.height-(border_thickness*2),
            spacing=5,
            padding=5,
            position=self.y+border_thickness
        )

        self.slider_height = heights[2]
        self.slider_spacing = (
            y_positions[2]
            - y_positions[1]
            - self.slider_height
        )

        self.preview_size = (heights[2]*3)+(self.slider_spacing*2)
        self.preview_positions = []

        self.slider_width = (
            self.width
            - self.preview_size * 2
            - 15
        )

        ##Colour sliders, text and previews
        i = 0
        for col_i, colour in enumerate(self.window.colours):

            ##Add text for each colour
            window = self.window
            text = RawText(
                self,
                x=self.x+7, y=y_positions[i],
                text=f"Colour {col_i+1}:",
                font=(window.font, heights[i]), 
                colour=3
            )
            self.colour_text.append(text)
            i += 1

            self.preview_positions.append(y_positions[i])
            for chan_i, channel in enumerate(colour):
                ##Change slider width based on element width
                slider_width = self.slider_width

                ##Add slider for each colour channel.
                slider = Slider(
                    self,
                    self.x+7, y_positions[i], slider_width, heights[i],
                    0, 255, channel
                )
                self.colour_sliders.append(slider)

                ##Add value text for each colour channel
                text = RawText(
                    self,
                    self.x+5+slider_width+5, y_positions[i], 
                    "Value", (self.window.font, heights[i]),
                    colour=3
                )
                self.channel_text.append(text)
                i += 1

        #region buttons
        ##Align and justify buttons.
        button_positions, button_widths = space_elements(
            elements=[2, 2, 3, 2],
            size=self.width,
            spacing=5,
            padding=7,
            position=self.x
        )

        ##Apply changes button
        self.apply_button = Button(
            self,
            button_positions[0], y_positions[i], button_widths[0], heights[i],
            "Apply", 13, action=self.apply
        )
        self.buttons.append(self.apply_button)

        ##Revert changes button
        self.reset_button = Button(
            self,
            button_positions[1], y_positions[i], button_widths[1], heights[i],
            "Reset", 13, action=self.reset
        )
        self.buttons.append(self.reset_button)

        ##Reset to defaults button
        self.default_button = Button(
            self,
            button_positions[2], y_positions[i], button_widths[2], heights[i],
            "Defaults", 13, action=self.defaults
        )
        self.buttons.append(self.default_button)

        ##Load button
        self.load_button = Button(
            self,
            button_positions[3], y_positions[i], button_widths[3], heights[i],
            "Load", 13, action=self.switch_palette
        )
        self.buttons.append(self.load_button)
        #endregion

        self.config = read_config("config.json")
        self.load_colours()

    ##Called every frame
    def update(self) -> None:
        super().update()

        ##Update colours for previews
        for i in range(0, len(self.colours)):
            self.colours[i] = ( self.colour_sliders[(i*3)+0].get_value(),
                                self.colour_sliders[(i*3)+1].get_value(),
                                self.colour_sliders[(i*3)+2].get_value())

        ##Check buttons clicked.
        for button in self.buttons:
            if button.clicked():
                button.action()

    def draw(self) -> None:
        super().draw()
        preview_size = self.preview_size

        ##Draw preview square of each colour
        i = 0
        for colour in self.colours:
            for channel in range(0, len(colour)):
                self.channel_text[(i*3)+channel].text = str(colour[channel])

            ##Base colour preview rect.
            preview_rect = [
                self.x+self.width-self.preview_size-self.border_thickness-5,
                self.preview_positions[i],
                preview_size, preview_size
            ]

            ##Background border rect
            pg.draw.rect(self.window.screen, (0,0,0), preview_rect)

            ##Coloured preview
            pg.draw.rect(self.window.screen, self.colours[i],
                         [preview_rect[0]+self.border_thickness,
                          preview_rect[1]+self.border_thickness,
                          preview_rect[2]-(self.border_thickness*2),
                          preview_rect[3]-(self.border_thickness*2)])
            i += 1


    ##Apply selected colours to parent window
    def apply(self, save=True) -> None:
        self.window.colours = list(self.colours)

        all_text = self.channel_text + self.colour_text
        for text in all_text:
            text.colour = self.window.colours[3]
        
        if self.window.parent.colours:
            self.window.parent.set_colours(list(self.colours))

        if save:

            username = self.window.parent.user
            if not username:
                return

            ##Get path to user options file.
            user_options_path = f"{self.config.user_options_folder}{username}.json"

            ##If file exists, get contents.
            if os.path.exists(user_options_path):
                with open(user_options_path, "r") as file:
                    options = json.load(file)
                    options["colours"] = self.colours
                    file.close()
            else:
                ##Make new options if file does not exist.
                options = {"colours": self.colours}


            with open(user_options_path, "w") as file:
                json.dump(options, file)
                file.close()

            self.load_button.text.text = "user"


    ##Revert colours to last selection
    def reset(self) -> None:
        self.colours = list(self.window.colours)
        self.update_sliders()


    ##Revert selection to default
    def defaults(self) -> None:
        self.colours = self.config.default_colours
        self.update_sliders()
        self.apply(False)


    ##Update slider values to match colours
    def update_sliders(self) -> None:
        i = 0
        for colour in self.colours:
            for channel in colour:
                self.colour_sliders[i].set_value(channel)
                i += 1


    def load_colours(self) -> None:
        username = self.window.parent.user
        config = self.config
        default_colours = config.default_colours
        if not username:
            self.colours = default_colours
            self.update_sliders()
            self.apply(False)
            return

        user_options_path = f"{config.user_options_folder}{username}.json"
        
        ##Create palette file if one does not already exist.
        if not os.path.isfile(user_options_path):
            self.defaults()
            with open(user_options_path, "w+") as file:
                json.dump({"colours":default_colours}, file)
                file.close()
        else:
            with open(user_options_path, "r") as file:
                self.colours = json.load(file)["colours"]
                file.close
            self.update_sliders()
            self.apply(False)


    def load_palettes(self):
        palettes = []
        for palette in [i for i in os.listdir(self.palette_directory) if i[-5:] == ".json"]:
            with open(self.palette_directory+palette) as file:
                contents = file.read()
                palettes.append((palette[:-5], json.loads(contents)))
        return palettes

    def switch_palette(self):
        ##I have no idea why, but clicking the switch palette button
        ##calls this function twice, so the bool ugh stops it from
        ##actually running twice.
        self.ugh = not self.ugh
        if self.ugh:
            self.palette_index = (self.palette_index + 1) % len(self.palettes)
            self.colours = self.palettes[self.palette_index][1]
            self.load_button.text.text = self.palettes[self.palette_index][0]
            self.update_sliders()
            self.apply(False)
