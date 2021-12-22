import sys


sys.path.append('C:/Users/jrish/work/python-sdk/skylark_ai')
import time
from skylark.core.frame_process.websocket_client import Client, Service
import logging
import json
import websocket
import cv2
import threading
from multiprocessing import Process
import imutils
import base64
import numpy as np

token = "179961d3901780ea244d044b8fd85879589b7dcace0fb00c34e2317451a89010"

def on_message(ws, message):
    print(message)


def start_stream():
    try:
        i = 0
        print("called")
        start = time.time()
        client = Client(token, Service.FACE_RECOG, on_message, batch_size=1)
        client.connect()
        time.sleep(1)
        # vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        vid = cv2.VideoCapture("rtsp://admin:admin123@203.134.200.170:8000/cam/realmonitor?channel=12&subtype=0")
        fps = 15
        sampling_rate = 1
        client.set_batch_size(1)
        client.set_databaseID("2db2ae96-f341-4767-8e68-6ddd1c2f972b")
        while True:
            print("reading")
            print("sending")
            print(i)
            ret, frame = vid.read()
            sampling_rate  = 1
            print(sampling_rate)
            if ret:
                # frame = imutils.resize(frame, width=12)
                frame = cv2.resize(frame, (256,190), interpolation=cv2.INTER_LINEAR)
                encode_params = [cv2.IMWRITE_JPEG_QUALITY, 90]
                byte_array = cv2.imencode('.jpg', frame, encode_params)[1]
                # print(byte_array)
                client.websocket.send(json.dumps({
                    "fileSize": byte_array.__len__(),
                    "syncId": i,
                    "action": "start_frame"
                }))
                client.send_frame(byte_array)
                i = i+1
                time.sleep(1/sampling_rate)
                # if i==30:
                #     print(str(time.time() - start))
                #     break

    except Exception as e:
        print('error in process')
        print(e)
    


if __name__ == "__main__":
    try:
        p1= Process(target = start_stream)
        p1.start()

        while True:
            time.sleep(1)
            print("hello")
        
        
        # client.websocket.send("hello")

    except Exception as err:
        print(err)
        logging.error("mmain Error")
        print("connect failed")