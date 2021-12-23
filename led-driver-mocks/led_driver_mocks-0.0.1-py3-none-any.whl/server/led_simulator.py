import socketio

from .server import Server


class LedSimulator(Server):

    sio = socketio.Client()
    host = None

    def __init__(self, address, port):
        self.sio.on('connect', self.connect)
        self.sio.on('error', self.error)
        self.sio.on('disconnect', self.disconnect)
        self.connect_to_server(address, port)

    def connect_to_server(self, address, port):
        if not self.sio.connected:
            self.host = 'http://' + str(address) + ':' + str(port)
            self.sio.connect(self.host)

    def send_led_data(self, data):
        self.sio.emit('led_update', data)

    def connect(self):
        print(f'Successful connected to led simulator server {self.host}')

    def error(self, data):
        print('An error occurred: ' + str(data))

    def disconnect(self):
        print(f'Disconnected from server {self.host}')