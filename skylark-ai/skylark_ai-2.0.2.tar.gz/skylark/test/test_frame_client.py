
import sys


sys.path.append('C:/Users/jrish/work/python-sdk/skylark_ai')
# print(sys.path)

from skylark.core.clients import Service
from skylark.core.face_mask_stream import FaceMaskStreamClient
from skylark.core.face_detect_stream import FaceDetectStreamClient
from skylark.core.weapon_detection_stream import WeaponDetectionStreamClient
from skylark.core.facial_landmark_stream import FacialLandmarkStream
from skylark.core.lie_detection_stream import LieDetectionStreamClient
from skylark.core.night_day_stream import NightDayStreamClient
from skylark.core.cab_violence_stream import CabViolenceStreamClient
from skylark.core.face_recog_stream import FaceRecogStreamClient
from skylark.core.general_violence_stream import GeneralViolenceStreamClient
from skylark.core.pedestrian_detect_stream import PedestrianDetectionStreamClient
from skylark.core.crowd_counting_stream import CrowdCountingStreamClient
from skylark.core.dress_insights_stream import DressInsightStreamClient
from skylark.core.ensemble_license_ocr_stream import EnsembleLicenseOCRStreamClient
from skylark.core.city_wide_stream import CityWideStreamClient
import time
from skylark.utils.utils import is_connected
from threading import Thread
from skylark.core.multi_stream import MultiStreamer
from skylark.core.process_frames import ProcessFrameClient
import cv2




# user will add authorization token here
token = "abcd"

# user will send fps of incoming stream, size of batch that will be formed while processing ,

# user can continue to perform any further tasks as per need
if __name__ == '__main__':
    print("starting")
    frame_client = ProcessFrameClient(1, Service.FACE_DETECT, token)
    src = "rtsp://admin:admin123@203.134.200.170:8000/cam/realmonitor?channel=12&subtype=0"
    stream = cv2.VideoCapture(src, cv2.CAP_FFMPEG)
    ret, frame = stream.read()
    frame_client.process(frame)

try:
    i=0
    while True:
        print("in mian")
        # print(client.response_jsons)
        time.sleep(1)
except KeyboardInterrupt:
	print("exiting")
	exit()
	
