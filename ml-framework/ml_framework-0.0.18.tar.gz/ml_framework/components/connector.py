from ml_framework.base.base_component import BaseComponent


class Connector(BaseComponent):
    def __init__(self):
        pass

    def run(self, config) -> str:
        print("Connector")
        print(config)
        print("------")

        return super().run(config)
