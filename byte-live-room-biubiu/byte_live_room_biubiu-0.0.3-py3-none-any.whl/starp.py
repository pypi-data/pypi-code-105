from PySide6.QtWidgets import QApplication
from byte_live_room_biubiu.Widget import *
import sys


def run():
    app = QApplication([])

    widget = Widget()
    widget.resize(850, 670)
    widget.show()

    sys.exit(app.exec())


