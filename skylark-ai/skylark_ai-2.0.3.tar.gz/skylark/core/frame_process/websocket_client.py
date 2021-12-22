import websocket
import threading, time
from skylark.core.frame_process.utils import get_websocket_auth_token
from skylark.constants.constants import HOST
from enum import Enum
import logging
import ssl
import json
import numpy as np
import base64
from pymitter import EventEmitter





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
	Service.CROWD_COUNTING:"ensemble-license-ocr/",
	Service.DRESS_INSIGHTS: "dress-insights/",
	Service.ENSEMBLE_LICENSE_OCR: "ensemble-license-ocr/",

}



class Client:
    protocol = "wss://"
    route = "ws/"
    def __init__(self, token, service_name, on_message, batch_size=1):
        self.token = token
        self.service_name = service_name
        self.websocket_token = None
        self.websocket = None
        self.on_message = on_message
        self.batch_size=batch_size

    def _callback(self, callback, *args):
        if callback:
            try:
                callback(self, *args)

            except Exception as e:
                _logging.error("error from callback {}: {}".format(callback, e))
                if self.on_error:
                    self.on_error(self, e)

    def on_message_main(self, ws, message):
        print("BEFORE CALLBACK")
        if "results" in message:
            message = json.loads(message)
            print(message)
        self._callback(self.on_message, message)

    
    
    def on_close(self, ws):
        # print('disconnected from server')
        print ("Retry : %s" % time.ctime())
        time.sleep(10)
        self.connect()
    
    def on_open(self, ws):
        print("connnection established")
        self.set_batch_size(self.batch_size)
    
    def on_error(self, ws, error):
        print("ws error")
        logging.error("error")
        print(error)
        print ("Retry : %s" % time.ctime())
        time.sleep(3)
        self.connect()
    
    def set_batch_size(self, batch_size):
        print("setting batch size")
        while self.websocket is None:
            # if connection is closed we wait for reconnection
            print("none")
        try:
            self.websocket.send(json.dumps({
                "action": 'set_batch_size',
                "batchSize": batch_size
            }))
        except Exception as e:
            logging.log("error set batch")
    
    def set_databaseID(self, databaseID):
        print("setting database id")
        while self.websocket is None:
            # if connection is closed we wait for reconnection
            print("none")
        try:
            self.websocket.send(json.dumps({
                "action": 'set_database',
                "database_id": databaseID
            }))
        except Exception as e:
            logging.log("error set batch")

    def send_frame(self, bytes):
        self.websocket.send(bytes, websocket.ABNF.OPCODE_BINARY)

    
    def connect(self):
        try:
            if self.websocket_token is None:
                self.websocket_token = get_websocket_auth_token(self.token)
                print("WESOCKET TOKEN IS ")
                print(self.websocket_token)
                self.url = "wss://"+ HOST + "/" + self.route + self.service_name.get_uri()
                self.url = self.url + "?authorization=%s" % self.websocket_token
                print(self.url)
                self.websocket = websocket.WebSocketApp(self.url, on_open=self.on_open, on_error=self.on_error, on_message=self.on_message_main)
                wst = threading.Thread(target=self.websocket.run_forever, args=(None, {"cert_reqs": ssl.CERT_NONE}), kwargs={'ping_interval': 5, 'ping_timeout' : 2})
                wst.setDaemon(True)
                wst.start()
                # self.websocket.run_forever()
        except Exception as e:
            logging.error("connect error")
            print(e)



            


