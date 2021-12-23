from abc import ABC, abstractmethod


class Server(ABC):

    @abstractmethod
    def send_led_data(self, data):
        pass
