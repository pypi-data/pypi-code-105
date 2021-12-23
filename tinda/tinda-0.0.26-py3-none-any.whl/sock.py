import socket
import pyaudio
import select
import threading
import cv2
import pyautogui
import numpy
import pickle
import struct
import requests


class StreamServer:
    def __init__(self, host, port, number_of_connections=9, exit_key='q'):
        self.__host = host
        self.__port = port
        self.__number_of_connections = number_of_connections
        self.__taken_connections = 0
        self.__exit_key = exit_key
        self.__running = False
        self.__lock = threading.Lock()
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__bind()
    def __bind(self):
        self.__server.bind((self.__host, self.__port))
    def start(self):
        if self.__running:
            print("server is already running")
        else:
            self.__running = True
            server_thread = threading.Thread(target=self.__listen)
            server_thread.start()
    def __listen(self):
        self.__server.listen()
        while self.__running:
            self.__lock.acquire()
            x, y = self.__server.accept()
            if self.__taken_connections >= self.__number_of_connections:
                print("Number of connections limit reached.")
                x.close()
                self.__lock.release()
                continue
            else:
                self.__taken_connections += 1
                self.__lock.release()
                task = threading.Thread(target=self.__handle_client, args=(x, y))   
                task.start()
    def __handle_client(self, x, y):
        data_size = struct.calcsize('>L')
        data = b""
        while self.__running:
            break_loop = False
            while len(data) < data_size:
                rec = x.recv(4096)
                if rec == b'':
                    x.close()
                    self.__taken_connections -= 1
                    break_loop = True
                    break
                data += rec
            if break_loop:
                break
            pack = data[:data_size]
            data = data[data_size:]
            xx = struct.unpack('>L', pack)[0]
            while len(data) < xx:
                data += x.recv(4096)
            frame = data[:xx]
            data = data[xx:]
            f = pickle.loads(frame, fix_imports=True, encoding="bytes")
            f = cv2.imdecode(f, cv2.IMREAD_COLOR)
            cv2.imshow(str(y), f)
            if cv2.waitKey(1) == ord(self.__exit_key):
                x.close()
                self.__taken_connections -= 1
                break
    def stop(self):
        if self.__running:
            self.__running = False
            cc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cc.connect((self.__host, self.__port))
            cc.close()
            self.__lock.acquire()
            self.__server.close()
            self.__lock.release()
        else:
            print("Server is not running.")
    @staticmethod
    def getIp(): # get ip address
        localIP = socket.gethostbyname(socket.gethostname())
        publicIP = requests.get('http://ip.42.pl/raw').text
        return f"Local IP: '{localIP}', Public IP: '{publicIP}'"
    @staticmethod
    def run():
        local_ip = socket.gethostbyname(socket.gethostname())
        port = 6969
        print(f"Server is running on: IP '{local_ip}'  Port '{port}'")
        server = StreamServer(local_ip, port)
        task = threading.Thread(target=server.start)
        task.start()
        while input("") != "q":
            continue
        server.stop()


class StreamClient:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self._config()
        self.__running = False
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def _config(self):
        self.__encoding = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    def _get_frame(self):
        return None
    def _clear(self):
        cv2.destroyAllWindows()
    def _stream(self):
        self.__sock.connect((self.__host, self.__port))
        while self.__running:
            frame = self._get_frame()
            res, frame = cv2.imencode('.jpg', frame, self.__encoding)
            data = pickle.dumps(frame, 0)
            size = len(data)
            try:
                self.__sock.sendall(struct.pack('>L', size) + data)
            except ConnectionResetError:
                self.__running = False
            except ConnectionAbortedError:
                self.__running = False
            except BrokenPipeError:
                self.__running = False
            self._clear()
    def start(self):
        if self.__running:
            print("client stream is already running.")
        else:
            self.__running = True
            task = threading.Thread(target=self._stream)
            task.start()
    def stop(self):
        if self.__running:
            self.__running = False
        else:
            print("client stream is not running.")


class ScreenSharingClient(StreamClient):
    def __init__(self, host, port, x_resolution=1024, y_resolution=768):
        self.__x_resolution = x_resolution
        self.__y_resolution = y_resolution
        super(ScreenSharingClient, self).__init__(host, port)
    def _get_frame(self):
        x = pyautogui.screenshot()
        y = numpy.array(x)
        y = cv2.cvtColor(y, cv2.COLOR_BGR2RGB)
        y = cv2.resize(y, (self.__x_resolution, self.__y_resolution), interpolation=cv2.INTER_AREA)
        return y
    @staticmethod
    def run():
        ip = input("Enter server ip: ")
        port = input("Enter server port: ")
        client = ScreenSharingClient(ip, int(port))
        task = threading.Thread(target=client.start)
        task.start()
        while input("") != "q":
            continue
        client.stop()


class CamClient(StreamClient):
    def __init__(self, host, port, x_resolution=1024, y_resolution=576):
        self.__x_resolution = x_resolution
        self.__y_resolution = y_resolution
        self.__camera = cv2.VideoCapture(0)
        super(CamClient, self).__init__(host, port)
    def _config(self):
        self.__camera.set(3, self.__x_resolution)
        self.__camera.set(4, self.__y_resolution)
        super(CamClient, self)._config()
    def _get_frame(self):
        res, frame = self.__camera.read()
        return frame
    def _clear(self):
        self.__camera.release()
        cv2.destroyAllWindows()
    @staticmethod
    def run():
        pass


class VideoClient(StreamClient):
    def __init__(self, host, port, video, loop=True):
        self.__video = cv2.VideoCapture(video)
        self.__loop = loop
        super(VideoClient, self).__init__(host, port)
    def _config(self):
        self.__video.set(3, self.__x_resolution)
        self.__video.set(4, self.__y_resolution)
        super(VideoClient, self)._config()
    def _get_frame(self):
        res, frame = self.__video.read()
        return frame
    def _clear(self):
        self.__video.release()
        cv2.destroyAllWindows()
    @staticmethod
    def run():
        pass


class AudioClient:
    def __init__(self, host, port, audio_format=pyaudio.paInt16, channels=1, rate=44100, frames_chunk=4096):
        self.__host = host
        self.__port = port
        self.__audio_format = audio_format
        self.__channels = channels
        self.__rate = rate
        self.__frames_chunk = frames_chunk
        self.__send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__audio = pyaudio.PyAudio()
        self.__running = False
    def start(self):
        if self.__running:
            print('Streating Audio.')
        else:
            self.__running = True
            thread = threading.Thread(target=self.__clientStream)
            thread.start()
    def stop(self):
        if not self.__running:
            self.__running = False
        else:
            print('Client stream not found.')
    def __clientStream(self):
        self.__send_socket.connect((self.__host, self.__port))
        self.__stream = self.__audio.open(format=self.__audio_format, channels=self.__channels, rate=self.__rate, input=True, frames_per_buffer=self.__frames_chunk)
        while self.__running:
            self.__send_socket.send(self.__stream.read(self.__frames_chunk))

class AudioServer:
    def __init__(self, host, port, slots=9, audio_format=pyaudio.paInt16, channels=1, rate=44100, frames_chunk=4096):
        self.__host = host
        self.__port = port
        self.__slots = slots    
        self.__usedSlots = 0
        self.__audio_format = audio_format
        self.__channels = channels
        self.__rate = rate
        self.__frames_chunk = frames_chunk
        self.__audio = pyaudio.PyAudio()
        self.__serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__serverSocket.bind((self.__host, self.__port))
        self.__block = threading.Lock()
        self.__running = False
    def start(self):
        if self.__running:
            print('Streating Audio.')
        else:
            self.__running = True
            self.__stream = self.__audio(format=self.__audio_format, channels=self.__channels, rate=self.__rate, output=True, frames_per_buffer=self.__frames_chunk)
            thread = threading.Thread(target=self.__serverListening)
            thread.start()
    def __serverListening(self):
        self.__serverSocket.listen()
        while self.__running:
            self.block.acquire()
            connection, address = self.__serverSocket.accept()
            if self.__usedSlots >= self.__slots:
                print('Audio slots full.')
                connection.close()
                self.__block.release()
                continue
            else:
                self.__usedSlots += 1
            self.__block.release()
            thread = threading.Thread(target=self.__clientConnection, args=(connection, address,))
            thread.start()
    def __clientConnection(self, connection, address):
        while self.__running:
            data = connection.recv(self.__frames_chunk)
            self.__stream.write(data)
    def stop(self):
        if not self.__running:
            self.__running = False
            closingConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            closingConnection.connect((self.__host, self.__port))
            closingConnection.close()
            self.__block.acquire()
            self.__serverSocket.close()
            self.__block.release()
        else:
            print('Server stream not found.')


# LOCAL NETWORK TERMINAL CHAT
class TerminalChatClient:
    def __init__(self):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 6969
        try:
            self.sock = socket.socket()
            self.sock.connect((self.ip, self.port))
            task = threading.Thread(target=self._x, args=[self.sock])
            task.start()
            print("Connected to Terminal Chat Server")
            while True:
                messgae = input()
                if messgae == 'quit':
                    break
                self.sock.send(messgae.encode())
            self.sock.close()
        except Exception as e:
            print(f'Error connecting to server socket: Error >>> {e}')
            self.sock.close()
    def _x(self, c: socket.socket):
        while True:
            try:
                msg = c.recv(1024)
                if msg:
                    print(msg.decode())
                else:
                    c.close()
                    break
            except Exception as e:
                print(f'Error handling message from server: {e}')
                c.close()
                break

class TerminalChatServer:
    def __init__(self):
        self.connections = []
        self.port = 6969
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(('', self.port))
            self.sock.listen(9)
            print('Server running!')
            while True:
                x, y = self.sock.accept()
                self.connections.append(x)
                threading.Thread(target=self._x, args=[x, y]).start()
        except Exception as e:
            print(f'An error has occurred when instancing socket: {e}')
        finally:
            if len(self.connections) > 0:
                for i in self.connections:
                    self._remove_connection(i)
            self.sock.close()
    def _x(self, c: socket.socket, a: str):
        while True:
            try:
                message = c.recv(1024)
                if message:
                    print(f"{a[0]}:{a[1]} - {message.decode()}")
                    send_message = f"From {a[0]}:{a[1]} - {message.decode()}"
                    self._broadcast(send_message, c)
                else:
                    self._remove_connection(c)
                    break
            except Exception as e:
                print(f'Error to handle user connection: {e}')
                self._remove_connection(c)
                break
    def _broadcast(self, message: str, c: socket.socket) -> None:
        for i in self.connections:
            if i != c:
                try:
                    i.send(message.encode())
                except Exception as e:
                    print('Error broadcasting message: {e}')
                    self._remove_connection(i)
    def _remove_connection(self, c: socket.socket):
        if c in self.connections:
            c.close()
            self.connections.remove(c)


#LOCAL NETWORK AUDIO CHAT

class LocalAudioServer:
    def __init__(self):
            self.ip = socket.gethostbyname(socket.gethostname())
            while 1:
                try:
                    self.port = int(input('Enter port number: '))
                    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.s.bind((self.ip, self.port))
                    break
                except:
                    print("Couldn't bind to that port")
            self.connections = []
            self.accept_connections()
    def accept_connections(self):
        self.s.listen(100)
        print('Running on IP: '+self.ip)
        print('Running on port: '+str(self.port))
        while True:
            c, addr = self.s.accept()
            self.connections.append(c)
            threading.Thread(target=self.handle_client,args=(c,addr,)).start()
    def broadcast(self, sock, data):
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data)
                except:
                    pass
    def handle_client(self,c,addr):
        while 1:
            try:
                data = c.recv(1024)
                self.broadcast(c, data)
            except socket.error:
                c.close()




class LocalAudioClient:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while 1:
            try:
                self.target_ip = input("Enter Server's IP: ")
                self.target_port = int(input('Enter target port: '))
                self.s.connect((self.target_ip, self.target_port))
                break
            except:
                print("Couldn't connect to server")
        chunk_size = 1024 # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000
        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
        print("Connected to Server")
        # start threads
        receive_thread = threading.Thread(target=self.receive_server_data).start()
        self.send_data_to_server()
    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass
    def send_data_to_server(self):
        while True:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
            except:
                pass


