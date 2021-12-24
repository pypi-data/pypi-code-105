from cm_adb import server
from cm_adb.client import client
import unittest


class ServerTest(unittest.TestCase):
    def test_server(self):
        host, port = 'localhost', 1234
        serv = server.CMADBServer(host, port)

        serv._start()
        for i in range(3):
            message = f'Message #{i}'
            response = client(host, port, message)
            self.assertEqual(message, response)



if __name__ == '__main__':
    unittest.main()
