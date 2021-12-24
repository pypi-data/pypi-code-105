from ml_framework.base.base_component import BaseComponent


class Comparator(BaseComponent):
    def __init__(self):
        pass

    def run(self, config) -> str:
        print(config)

        return super().run(config)
