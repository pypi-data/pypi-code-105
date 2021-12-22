from skylark.core.streams import StreamClient

import cv2
import time
import asyncio
from skylark.core.clients import RealTimeClient
from skylark.core.clients import Service
import logging
from skylark.utils.utils import VideoGet
from bounding_box import bounding_box as draw_boxes
import numpy as np
import base64

class CityWideStreamClient(StreamClient):
    def __init__(self,id, fps, batch_size, sampling_rate, token, show_processed_stream=False,
        save_raw_frames=False, scale_percent=100, quality=100, stream=0):
        self.fps = fps
        self.frames = []
        self.json = ""
        self.syncid = -1
        self.batch_size = batch_size
        self.sampling_rate = sampling_rate
        self.sample_length = int(fps / sampling_rate)
        self.delay_sec = 1 / self.fps
        self.stream = stream
        self.vid = VideoGet(self.stream).start()
        self.token = token
        print("real time hit")
        self.client = RealTimeClient(Service.CITY_WIDE, self.on_receive, batch_size, self.on_network_status_change, self.token)
        print("hit done")
        self.response_jsons = []
        self.show_processed_stream = show_processed_stream
        self.save_raw_frames = save_raw_frames
        self.scale_percent = scale_percent
        self.quality = quality
        self.id = id
        self.createTasks()
        self.classes = {
            "0": "bus",
            "1": "rickshaw",
            "2": "motorbike",
            "3": "car",
            "4": "three-wheelers(CNG)",
            "5": "pickup",
            "6": "mini-van",
            "7": "suv",
            "8": "van",
            "9": "taxi",
            "10": "truck",
            "11": "bicycle",
            "12": "police-car",
            "13": "ambulance",
            "14": "human-hauler",
            "15": "wheel-barrow",
            "16": "minibus",
            "17": "auto-rickshaw",
            "18": "army-vehicle",
            "19": "scooter",
            "20": "garbage-van",
            
            "21": "skirt",
            "22": "short sleeve top",
            "23": "vest",
            "24": "trousers",
            "25": "long sleeve top",
            "26": "shorts",
            "27": "long sleeve outwear",
            "28": "vest dress",
            "29": "long sleeve dress",
            "30": "short sleeve dress",
            "31": "sling dress",
            "32": "short sleeve outwear",
            "33": "sling",

            "34": "pistol",
            "35": "rifle",
            "36": "stick",
            "37": "knife",
            "38": "blade",
            "39": "launcher",
            "40": "hammer",

            "41": "human",

            "42": "face",

            "43": "license plate",

            "44": "0",
            "45": "1",
            "46": "2",
            "47": "3",
            "48": "4",
            "49": "5",
            "50": "6",
            "51": "7",
            "52": "8",
            "53": "9",
            "54": "A",
            "55": "B",
            "56": "C",
            "57": "D",
            "58": "E",
            "59": "F",
            "60": "G",
            "61": "H",
            "62": "I",
            "63": "J",
            "64": "K",
            "65": "L",
            "66": "M",
            "67": "N",
            "68": "O",
            "69": "P",
            "70": "Q",
            "71": "R",
            "72": "S",
            "73": "T",
            "74": "U",
            "75": "V",
            "76": "W",
            "77": "X",
            "78": "Y",
            "79": "Z"
        }
    
    def np_from_json(self, obj, prefix_name=""):
            return np.frombuffer(base64.b64decode(obj["{}_frame".format(prefix_name)].encode("utf-8")),dtype=np.dtype(obj["{}_dtype".format(prefix_name)])).reshape(
                obj["{}_shape".format(prefix_name)])

    def scale_coordinates(self, json):
            # print("scaling")
            # print(json)
            # output = json['results']
            # print(type(output))
            # print("outptu")
            # print(output)
            # license_plates = self.np_from_json(output['license_plates'])
            # faces_detected = self.np_from_json(output['faces_detected'])
            # vehicle_output = self.np_from_json(output['vehicle_output'])
            # print(vehicle_output)

            # ocr_output = output['ocr_output']
            # new_result = {}
            # new_result['license_plates']= license_plates
            # new_result['ocr_output'] = ocr_output
            # new_result['vehicle_output'] = vehicle_output
            # new_result['faces_detected'] = faces_detected

            # json['results'] = output
            print("################################################  converted json #################################################")
            print(json)
    # def draw_boxes(self, frame, coord_list, color, thickness):
    #     for coords in coord_list:
    #         start_point = (int(coords[0]),int(coords[1]))
    #         end_point = (int(coords[2]),int(coords[3]))
    #         frame = cv2.rectangle(frame,start_point,end_point, color, 3)
    #     return frame


    async def show_stream(self):
        # on message receive from websocket, we parse json response and show stream using cv2
        if self.show_processed_stream:
            while True:
                try:
                    # print("######################################################show stream")
                    if len(self.response_jsons) == 0:
                        # if no responses then keep waiting for some message to be received
                        print("waiting inside show stream")
                        print(len(self.response_jsons))
                        await asyncio.sleep(1)
                        continue
                    # print("#############################  have content  #############################")
                    print(len(self.response_jsons))
                    # take out one of the response from beginning and apply the result to the frames
                    response = self.response_jsons.pop(0)
                    # syncid is used to maintain between sent and received frames
                    self.syncid = self.syncid + self.batch_size
                    syncids = response["sync"]
                    if self.syncid != syncids[-1]:
                        # if syncid sent and received for a particular response is not same then acheive sync
                        print("##########################not in sync:###################################")
                        print(self.syncid)
                        print(syncids[-1])
                        if self.syncid > syncids[-1]:
                            # discarding results
                            while self.syncid != syncids[-1]:
                                syncids = response["sync"]
                                self.response_jsons.pop(0)
                        else:
                            # discarding frames
                            while self.syncid != syncids[-1]:
                                self.frames.pop(0)
                                self.syncid = self.syncid + 1
                        continue
                    
                except Exception as e:
                    logging.error("Error")
                    exit()

                else:
                    # when in sync move further
                    print("############### in sync ###########################")
                    try:
                        self.delay_sec = 1/(self.fps + len(self.frames)/5)
                        results = response["results"]
                        # results = results["final_output"]
                        print("resutls are")
                        print(type(results))

                        for i in range(self.sample_length):
                            frame = self.frames.pop(0)
                            start_time = time.time()
                            ped_det_output = results['people_detected']
                            print("PED")
                            print(ped_det_output)
                            for output in ped_det_output:
                                if output[0][0] != -1:
                                    print(output)
                                    x1 = int(output[0][0]* 100 / self.scale_percent)
                                    y1 = int(output[0][1]* 100 / self.scale_percent)
                                    x2 = int(output[1][0]* 100 / self.scale_percent)
                                    y2 = int(output[1][1]* 100 / self.scale_percent)
                                    draw_boxes.add(frame, x1, y1, x2, y2, self.classes[str(output[2][0])])
                            ped_det_output = results['faces_detected']
                            print("PED")
                            print(ped_det_output)
                            for output in ped_det_output:
                                if output[0][0] != -1:
                                    print(output)
                                    x1 = int(output[0][0]* 100 / self.scale_percent)
                                    y1 = int(output[0][1]* 100 / self.scale_percent)
                                    x2 = int(output[1][0]* 100 / self.scale_percent)
                                    y2 = int(output[1][1]* 100 / self.scale_percent)
                                    draw_boxes.add(frame, x1, y1, x2, y2, self.classes[str(output[2][0])])
                            ped_det_output = results['vehicle_output']
                            print("PED")
                            print(ped_det_output)
                            for output in ped_det_output:
                                if output[0][0] != -1:
                                    print(output)
                                    x1 = int(output[0][0]* 100 / self.scale_percent)
                                    y1 = int(output[0][1]* 100 / self.scale_percent)
                                    x2 = int(output[1][0]* 100 / self.scale_percent)
                                    y2 = int(output[1][1]* 100 / self.scale_percent)
                                    draw_boxes.add(frame, x1, y1, x2, y2, self.classes[str(output[2][0])])
                            ped_det_output = results['license_plates']
                            print("PED")
                            print(ped_det_output)
                            for output in ped_det_output:
                                if output[0][0] != -1:
                                    print(output)
                                    x1 = int(output[0][0]* 100 / self.scale_percent)
                                    y1 = int(output[0][1]* 100 / self.scale_percent)
                                    x2 = int(output[1][0]* 100 / self.scale_percent)
                                    y2 = int(output[1][1]* 100 / self.scale_percent)
                                try:
                                    ocr_text = ocr_output[idx][0].decode()
                                except Exception as e:
                                    ocr_text = 'OCR Failed'                                    
                                    draw_boxes.add(frame, x1, y1, x2, y2, ocr_text)
                            cv2.imshow(str(self.id), frame)
                            cv2.waitKey(1)
                            time_spent = time.time() - start_time
                            rem_time = max(self.delay_sec - time_spent, 0)
                            await asyncio.sleep(rem_time)

                    except Exception as e:
                        logging.exception("Error")
                        print("ex in city wide")
                        exit()
