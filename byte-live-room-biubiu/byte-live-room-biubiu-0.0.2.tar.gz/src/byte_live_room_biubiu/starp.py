from PySide6.QtWidgets import QApplication
from Widget import Widget
import sys


def run():
    app = QApplication([])

    widget = Widget()
    widget.resize(850, 670)
    widget.show()

    sys.exit(app.exec())

#
# if __name__ == "__main__":
#     run()
#
