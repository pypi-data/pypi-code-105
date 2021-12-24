from qdk.main import QDK


class CMQDK(QDK):
    def zoom_app(self):
        self.execute_method('zoom_app')
