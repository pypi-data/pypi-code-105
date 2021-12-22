import sys


sys.path.append('C:/Users/jrish/work/python-sdk/skylark_ai')
from skylark.constants.constants import WEBSOCKET_AUTH_API
import requests
import socket
REMOTE_SERVER = "one.one.one.one"

import queue
from threading import Thread
import cv2
from enum import Enum

class Service(Enum):
	FACE_MASK = 1,
	FACE_DETECT = 2,
	FACIAL_LANDMARK = 3,
	WEAPON_DETECTION = 4,
	LIE_DETECTION = 5,
	NIGHT_DAY = 6,
	CAB_VIOLENCE = 7,
	TEMPORAL = 8,
	FACE_RECOG = 9,
	GENERAL_VIOLENCE=10,
	PEDESTRIAN_DETECTION=11,
	CROWD_COUNTING=12,
	DRESS_INSIGHTS = 13,
	ENSEMBLE_LICENSE_OCR=14,
	CITY_WIDE=15,

	def get_uri(self):
		return service_uri_map.get(self, None)


service_uri_map = {
	Service.FACE_MASK: "face-mask/",
	Service.FACE_DETECT: "face-detect/",
	Service.FACIAL_LANDMARK: "facial-landmark/",
	Service.WEAPON_DETECTION: "weapon-detection/",
	Service.LIE_DETECTION: "lie-detection/",
	Service.NIGHT_DAY: "night-day/",
	Service.CAB_VIOLENCE: "cab-violence/",
	Service.TEMPORAL:"process-temporal/",
	Service.FACE_RECOG: "face-recog-bulk/",
	Service.GENERAL_VIOLENCE:"violence-detection/",
	Service.PEDESTRIAN_DETECTION:"pedestrian-detection/",
	Service.CROWD_COUNTING:"crowd-counting/",
	Service.DRESS_INSIGHTS: "dress-insights/",
	Service.ENSEMBLE_LICENSE_OCR: "ensemble-license-ocr/",

}

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src, cv2.CAP_FFMPEG)
        self.q = queue.Queue()
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):    
        thread = Thread(target=self.get, args=())
        thread.setDaemon(True)
        thread.start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                ret, frame = self.stream.read()
                if not ret:
                    self.stopped = True
                if not self.q.empty():
                    try:
                        self.q.get_nowait()
                    except queue.Empty:
                        pass
                self.q.put(frame)
                self.frame = frame
                # (self.grabbed, self.frame) = self.stream.read()


    def stop(self):
        self.stopped = True

    def read(self):
        return self.q.get()

def get_websocket_auth_token(token):
    try:
        print(token)
        '''
        changes --jash jain
        '''
        #changed the response so that when an api key(token) is passed a websocket token is retrieved
        response = requests.post(WEBSOCKET_AUTH_API,data={'api_key':token})
        if response.status_code == 201:
            print("hello")
            print(response.json())
            return response.json().get('key')
        else:
            return None
    except socket.gaierror:
        print("Internet not found")


def get_bytes_from_file(filename):
    return open(filename, "rb").read()

def is_connected(hostname="one.one.one.one"):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except:
     pass
  return False
