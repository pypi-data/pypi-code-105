from omnitools import FTPESS, FTPS
from collections import deque
import threading
import time
import os


class FTPRelayFO:
    def __init__(self, length: int = 0):
        self.buffer = deque()
        self.name = None
        self.closed = False
        self.timeout = 5
        self.parts = 0
        self.length = length
        self.has_length = not not length
        self.red = 0

    def tell(self):
        return self.red

    def __len__(self):
        return self.length

    def __iter__(self):
        return self.read()

    def _read(self):
        tried = 0
        while True:
            try:
                return self.buffer.popleft()
            except IndexError:
                if self.closed:
                    return memoryview(b"")
                if tried < self.timeout:
                    tried += 1
                    time.sleep(1)
            except Exception as e:
                print(e)

    def read(self, n: int = -1, do_red=True):
        if n == -1:
            print(-1)
            return self._read()
        red = self._read()
        l = len(red)
        if l == 0:
            return red.tobytes()
        if l == n:
            if do_red:
                self.red += n
            return red.tobytes()
        elif l > n:
            self.buffer.appendleft(red[n:])
            if do_red:
                self.red += n
            return red[:n].tobytes()
        else:
            red = red.tobytes()
            if do_red:
                self.red += l
            while l < n:
                _red = self.read(n-l, False)
                _l = len(_red)
                l += _l
                red = red+_red
                if do_red:
                    self.red += _l
                if not _red:
                    return red
            return red

    def write(self, s: bytes):
        _ = len(s)
        self.buffer.append(memoryview(s))
        self.parts += 1
        if not self.has_length:
            self.length += _
        return _

    def fileno(self):
        raise AttributeError("do not use sendfile()")

    def close(self):
        self.closed = True

    def flush(self):
        pass


def fake_remote_server_setup(server_type, credentials):
    if not credentials:
        credentials = ["foxe6"]*2
    port = 8022
    users = credentials+["elradfmwMT"]
    remote_homebase = os.path.abspath(r"s2")
    s2 = server_type(port=port)
    s2.server.max_cons = 10
    s2.server.max_cons_per_ip = 10
    homedir = os.path.join(remote_homebase, users[0])
    os.makedirs(homedir, exist_ok=True)
    s2.handler.authorizer.add_user(*users[:2], homedir, users[-1])
    if issubclass(server_type, FTPESS):
        s2.handler.certfile = os.path.join(remote_homebase, "foxe2.pem")
        s2.handler.tls_control_required = True
        s2.handler.tls_data_required = True
    s2.handler.passive_ports = range(51200, 52200)
    s2.configure()
    p2 = threading.Thread(target=s2.start)
    p2.daemon = True
    p2.start()
    return ["127.0.0.1", port], credentials


def fake_ftpes_remote_server_setup(credentials: list = None):
    return fake_remote_server_setup(FTPESS, credentials)


def fake_ftps_remote_server_setup(credentials: list = None):
    return fake_remote_server_setup(FTPS, credentials)


