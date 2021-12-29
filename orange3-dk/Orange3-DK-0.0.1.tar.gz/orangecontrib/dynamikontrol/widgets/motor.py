from AnyQt.QtWidgets import QLabel
from Orange.widgets.widget import OWWidget
from orangewidget.widget import OWBaseWidget, Output
from orangewidget.settings import Setting
from orangewidget import gui
from dynamikontrol import Module


class Motor(OWWidget):
    name = 'Motor'
    icon = 'icons/motor.png'
    description = '''Initialize a motor module. 모터 모듈을 초기화합니다.'''
    want_main_area = False

    module = None

    def __init__(self):
        super().__init__()

        self.optionsBox = gui.widgetBox(self.controlArea, 'Controller')

        # label = QLabel('Hello, Motor!')
        # self.optionsBox.layout().addWidget(label)

        gui.button(self.optionsBox, self, 'Run', callback=self.run)
        gui.button(self.optionsBox, self, 'Reset', callback=self.reset)

        try:
            self.module = Module()
            self.Outputs.module.send(self.module)
        except:
            print('Module is not connected!')

    class Outputs:
        module = Output('Module', object, auto_summary=False)

    def run(self):
        if self.module is None:
            return

        self.Outputs.module.send(self.module)

    def reset(self):
        if self.module is None:
            return

        self.module.motor.angle(0)

    def onDeleteWidget(self):
        if self.module is None:
            return

        self.module.disconnect()
        self.module = None
        super().onDeleteWidget()



if __name__ == '__main__':
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0
    WidgetPreview(Motor).run()
