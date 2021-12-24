import socketserver
import threading


class CMADBServerHandler(socketserver.ThreadingMixIn,
                         socketserver.BaseRequestHandler):
    """ Обработчик принимаемых данных"""
    def handle(self):
        data = self.request.recv(1024)
        threading.current_thread()
        self.request.sendall(data)


class CMADBServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """ Сервер, который поднимается вместе с программой, если он работает,
    значит, программа запущена. """
    def __init__(self, ip, port):
        super().__init__((ip, port), CMADBServerHandler)

    def _start(self):
        """ Логику по запуске сервера собираем для удобства здесь """
        thread_server = threading.Thread(target=self.serve_forever, args=())
        thread_server.daemon = True  # Что бы точно сдох при закрытии ПО
        thread_server.start()
