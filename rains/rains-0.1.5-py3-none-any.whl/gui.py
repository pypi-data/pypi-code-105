
from rains.common.const import ConstPath

from rains.gui.gui_running import GuiRunning

print(ConstPath.ROOT)

gui: GuiRunning = GuiRunning()
gui.running()
