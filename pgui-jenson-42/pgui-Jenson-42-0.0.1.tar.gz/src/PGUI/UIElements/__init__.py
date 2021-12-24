"""Adds UI elements based on pygame."""

from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

from PGUI.UIElements.button       import Button
from PGUI.UIElements.colourpicker import ColourPicker
from PGUI.UIElements.dropdown     import DropDown
from PGUI.UIElements.fpsdisplay   import FPSDisplay
from PGUI.UIElements.image        import Image
from PGUI.UIElements.inputfield   import InputField
from PGUI.UIElements.panel        import Panel
from PGUI.UIElements.slider       import Slider
from PGUI.UIElements.text         import RawText, WrappedText
from PGUI.UIElements.titlescreen  import TitleScreen
from PGUI.UIElements.togglebutton import ToggleButton
from PGUI.UIElements.tooltip      import Tooltip