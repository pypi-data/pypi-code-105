#!/tools/common/pkgs/python/3.6.3/bin/python3.6
"""
  Copyright (c) 2016- 2021, Wiliot Ltd. All rights reserved.

  Redistribution and use of the Software in source and binary forms, with or without modification,
   are permitted provided that the following conditions are met:

     1. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.

     2. Redistributions in binary form, except as used in conjunction with
     Wiliot's Pixel in a product or a Software update for such product, must reproduce
     the above copyright notice, this list of conditions and the following disclaimer in
     the documentation and/or other materials provided with the distribution.

     3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
     may be used to endorse or promote products or services derived from this Software,
     without specific prior written permission.

     4. This Software, with or without modification, must only be used in conjunction
     with Wiliot's Pixel or with Wiliot's cloud service.

     5. If any Software is provided in binary form under this license, you must not
     do any of the following:
     (a) modify, adapt, translate, or create a derivative work of the Software; or
     (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
     discover the source code or non-literal aspects (such as the underlying structure,
     sequence, organization, ideas, or algorithms) of the Software.

     6. If you create a derivative work and/or improvement of any Software, you hereby
     irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
     royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
     right and license to reproduce, use, make, have made, import, distribute, sell,
     offer for sale, create derivative works of, modify, translate, publicly perform
     and display, and otherwise commercially exploit such derivative works and improvements
     (as applicable) in conjunction with Wiliot's products and services.

     7. You represent and warrant that you are not a resident of (and will not use the
     Software in) a country that the U.S. government has embargoed for use of the Software,
     nor are you named on the U.S. Treasury Department's list of Specially Designated
     Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
     You must not transfer, export, re-export, import, re-import or divert the Software
     in violation of any export or re-export control laws and regulations (such as the
     United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
     and use restrictions, all as then in effect

   THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
   OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
   WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
   QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
   IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
   ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
   OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
   FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
   (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
   (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
   (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
   (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
"""
'''
Created on Oct 24, 2021

@author: davidd
'''
import pickle
from numpy.core._multiarray_umath import arange
from urllib.parse import quote
import jwt
import numpy
import requests
from os import _exit, makedirs, mkdir, environ
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pygubu
from multiprocessing import Queue
from threading import Thread, Lock
from time import sleep
import time
import queue
import csv
import datetime
from ConfigsGui import ConfigsGui, DEFAULT_CONFIG
from ComConnect import ComConnect, GO, CONTINUE, CONNECT_HW, READ, popup_message
from traceback import print_exc
from json import load, dump, dumps, loads
import argparse
import http.client
from sys import path, exit
from os.path import exists, isfile, abspath, dirname, join, isdir, basename
path.append(abspath(dirname(join('..', '..', '..', '..', 'pywiliot_internal'))))
from pywiliot_internal.wiliot.wiliot_testers.tester_utils import *
from pywiliot_internal.wiliot.packet_data_tools.process_encrypted_packets import estimate_diff_packet_time

mutex = Lock()
calibMutex = Lock()
recvDataMutex = Lock()

RAW = 'raw'
TIME = 'time'

DEF_NUM_OF_TAGS = 2

PREAMBLE_BYTES = 10
NIBS_IN_BYTE = 2
ADV_ADDR_START = 0
ADV_ADDR_END = 6
CRC_START = 29
# PAYLOAD_START = 8
PAYLOAD_START = 8

CSV_FILE_NAME = 'packets.csv'
OUTPUT_DIR = 'logs'

# CONNECT_HW = 'Connect Hw'
# GO = 'Go'
# CONTINUE = 'Continue'

CSV_COLUMNS = ['raw', 'time']
ID_CSV_COLUMNS = ['ext_id', 'chamber']
CSV_DATABASE_COLUMNS = ['timestamp', 'num of tags', 'tags answered', '% responding', 'num of packets', 'test duration [sec]', 'TTFP-AVG [sec]', 'TTFP-STD [sec]', 'TTFP-Min [sec]', 'TTFP-Max [sec]', 'TBP-AVG [sec]', 'TBP-STD [sec]', 'TBP-Min [sec]', 'TBP-Max [sec]', 'channel', 'energizing pattern', 'total time', 'on time', 'attenBle [db]', 'attenLoRa [db]', 'GTIN', 'reel']

TOKEN_FILE_NANE = '.token.pkl'

class SampleTest(object):
    goButtonState = CONNECT_HW
    comConnect = None
    configsGui = None
    comTtk = None
    configsTtk = None
    testBarcodesThread = None
    finishThread = None
    closeChambersThread = None
    gatewayDataReceive = None
    token = None
    claimSet = None
    testFinished = True
    closeRequested = False
    debugMode = False
    testGo = False
    testStop = False
    testTime = 0
    tagsCount = 0
    packetsCount = 0
    testStartTime = 0
    sleep = 0
    curAtten = 0
    defaultDict = {}
    packetDict = {}
    packetsDict = {}
    dataBaseDict = {}
    runDataDict = {}
    params = {}
    barcodesRead = {}
    tagsFinished = {}
    badPreambles = []
    numOfTags = DEF_NUM_OF_TAGS

    def __init__(self, debugMode=False, calib=None, low=None, high=None, step=None):

        self.calib = calib
        self.low = low
        self.high = high
        self.step = step
        
        if isfile(join('configs', '.defaults.json')):
            with open(join('configs', '.defaults.json'), 'r') as defaultComs:
                self.defaultDict = load(defaultComs)

        self.check_token()
        self.popup_login()
        self.update_data()
        # self.get_token()

        self.builder = builder = pygubu.Builder()
        self.debugMode = debugMode

        self.comConnect = ComConnect(topBuilder=builder)
        self.configsGui = ConfigsGui()

    def gui(self):
        self.set_gui()

        self.ttk.mainloop()

    def set_gui(self):
        uifile = join(abspath(dirname(__file__)), 'utils', 'sample_test.ui')
        self.builder.add_from_file(uifile)

        imgPath = join(abspath(dirname(__file__)), '.')
        self.builder.add_resource_path(imgPath)
        imgPath = join(abspath(dirname(__file__)), 'utils')
        self.builder.add_resource_path(imgPath)

        missingComPort = self.comConnect.choose_com_ports(self.defaultDict)

        if missingComPort:
            popup_message('Default com ports not available, check connections.', title='Warning')

        self.ttk = Tk()

        self.ttk.eval('tk::PlaceWindow . center')
        self.ttk.title("Wiliot Sample Test")
        self.mainWindow = self.builder.get_object('mainwindow', self.ttk)
        self.ttk.protocol("WM_DELETE_WINDOW", self.close)
        self.builder.connect_callbacks(self)

        configs = self.configsGui.get_configs()
        self.builder.get_object('test_config')['values'] = [key for key, item in configs.items() if isinstance(item, dict)]

        self.set_gui_defaults()

    def go(self):
        if self.finishThread is not None and self.finishThread.is_alive():
            self.finishThread.join()
        self.goButtonState = goButtonState = self.builder.tkvariables.get('go').get()
        self.builder.get_object('go')['state'] = 'disabled'
        if goButtonState == CONNECT_HW:
            self.connectThread = Thread(target=self.comConnect.connect_all, args=([False]))
            self.connectThread.start()
            # self.comConnect.connect_all(gui=False)
        elif goButtonState == READ:
            if self.tagsCount == 0:
                self.comConnect.reset_test_barcodes()
            indexes = self.get_missing_ids_chambers()
            self.testBarcodesThread = Thread(target=self.comConnect.read_scanners_barcodes, args=([indexes]))
            self.testBarcodesThread.start()
        elif goButtonState == GO:
            self.numOfPackets = 0
            self.totalNumOfUnique = 0
            self.avgUnique = 1
            self.badPreambles = []
            self.packetsDict = {}
            self.change_params_state(state='disabled')
            self.barcodesRead = self.comConnect.get_barcodes()
            self.packetsCount = 0
            self.numOfTags = int(self.builder.tkvariables.get('numTags').get())
            self.testId = time.time()
            self.update_params()
            self.testStartTime = time.time()
            if self.calib != None and self.calib.lower() in ['ble', 'lora']:
                self.calibModeThread = Thread(target=self.calib_mode, args=())
                self.calibModeThread.start()
            else:
                self.sendCommandThread = Thread(target=self.send_gw_commands, args=())
                self.sendCommandThread.start()
        elif goButtonState == CONTINUE:
            self.barcodesRead = self.comConnect.get_barcodes()
            self.change_params_state(state='disabled')
            self.sendCommandThread = Thread(target=self.send_gw_commands, args=())
            self.sendCommandThread.start()
            
    def get_missing_ids_chambers(self):
        lastBarcodes = self.comConnect.get_barcodes()
        indexes = list(range(self.comConnect.get_num_of_barcode_scanners()))
        if len(lastBarcodes) > 0:
            usedIndexes = list(lastBarcodes.values())
            indexes = [index for index in indexes if index not in usedIndexes]
        return indexes
    
    def force_go(self):
        if self.builder.get_variable('forceGo').get() == '1':
            indexes = self.get_missing_ids_chambers()
            self.closeChambersThread = Thread(target=self.comConnect.close_chambers, args=([indexes]))
            self.closeChambersThread.start()
            self.builder.tkvariables.get('go').set(GO)
        else:
            self.comConnect.update_go_state()
        

    def calib_mode(self):
        self.testFinished = False
        attens = arange(float(self.low), float(self.high) + float(step), float(self.step))
        for i in attens:
            calibMutex.acquire()
            self.totalNumOfUnique = 0
            self.avgUnique = 1
            self.packetDict = {}
            self.curAtten = i
            self.packetsCount = 0
            self.tagsFinished = {}
            self.testGo = True
            if self.calib.lower() == 'ble':
                self.params['attenBle'] = self.curAtten
                self.dataBaseDict['attenBle [db]'] = self.curAtten
            elif self.calib.lower() == 'lora':
                self.dataBaseDict['attenLoRa [db]'] = self.curAtten
                self.params['attenLoRa'] = self.curAtten
            self.sendCommandThread = Thread(target=self.send_gw_commands, args=())
            self.sendCommandThread.start()
            self.sendCommandThread.join()
            sleep(self.sleep)

        calibMutex.acquire()
        self.calib_mode_post_process()
        self.comConnect.open_chambers()
        self.builder.tkvariables.get('numTags').set(self.numOfTags)
        self.builder.tkvariables.get('go').set(READ)
        self.comConnect.reset_test_barcodes()
        self.builder.get_object('connect')['state'] = 'enabled'
        self.builder.get_object('read_qr')['state'] = 'enabled'
        calibMutex.release()
        popup_message('Sample Test - Calib Mode Finished running.')

    def calib_mode_post_process(self):

        testDir = datetime.datetime.fromtimestamp(self.testId).strftime('%d%m%y_%H%M%S')
        mkdir(join(OUTPUT_DIR, testDir))
        commonRunName = self.reelId + '_' + testDir
        uniqueValid = []
        with open(join(OUTPUT_DIR, testDir, f'{commonRunName}@packets_data_calib_mode.csv'), 'w+', newline='') as newCsv, \
             open(join(OUTPUT_DIR, testDir, f'{commonRunName}@unique_data.csv'), 'w+', newline='') as newTagsCsv:
            writer = csv.DictWriter(newCsv, fieldnames=['advAddress', 'status', 'rawData', 'attenuation'])
            writer.writeheader()
            for atten, runData in self.packetsDict.items():
                for preamble, data in runData.items():
                    if len(data['packets']) > 0:
                        for packet in data['packets']:
                            packetRaw = packet['raw'].split('(')[1].split(')')[0].strip(' "')
                            tagRow = {'advAddress': packetRaw[ADV_ADDR_START * NIBS_IN_BYTE:ADV_ADDR_END * NIBS_IN_BYTE],
                                      'status': 'PASSED',
                                      'rawData': packet,
                                      'attenuation': atten}
                            writer.writerows([tagRow])

                    uniqueValid.append({'preamble': preamble, 'tbp': data['tbp'], 'ttfp': data['ttfp'], 'ext ID': data['ext ID'], 'reel':data['reel'], 'attenuation':atten})

            writer = csv.DictWriter(newTagsCsv, fieldnames=uniqueValid[0].keys())
            writer.writeheader()
            writer.writerows(uniqueValid)

    def stop(self):
        if self.testGo:
            self.closeRequested = True
            recvDataMutex.acquire()
            self.closeRequested = False
            recvDataMutex.release()
        if not self.testFinished:
            self.builder.get_object('go')['state'] = 'disabled'
            self.builder.get_object('stop')['state'] = 'disabled'
            self.finishThread = Thread(target=self.finished, args=([True]))
            self.finishThread.start()

    def add(self):
        self.barcodesRead = self.comConnect.get_barcodes()
        newTag = self.builder.tkvariables.get('addTag').get()
        if not newTag.split(',')[0].strip() in self.barcodesRead.keys():
            # self.builder.get_object('scanned').insert(END, newTag)
            # self.barcodesRead[newTag.split(',')[0].strip()] = newTag.split(',')[1].strip()
            # self.comConnect.set_barcodes(self.barcodesRead)
            if len(newTag.split(',')) < 2:
                popup_message(f'Missing chamber index, add chamber index after a comma.', title='Error')
                return
            curId = newTag.split(',')[0].strip()
            scanIndex = int(newTag.split(',')[1].strip())
            if (scanIndex + 1) > self.comConnect.get_num_of_barcode_scanners():
                popup_message(f'Chamber number {scanIndex} not exists.', title='Error')
                return

            barcodes = self.builder.get_object('scanned').get(0, END)
            if any([barcode for barcode in barcodes if int(barcode.split()[1].strip()) == scanIndex]):
                popup_message(f'Chamber {scanIndex} tag already scanned.', title='Error')
                return
            # print(scanIndex)

            self.builder.tkvariables.get('addTag').set('')
            popupThread = Thread(target=popup_message, args=('Chambers are closing!!\nWatch your hands!!!', 'Warning', ("Helvetica", 18)))
            popupThread.start()
            popupThread.join()
            self.comConnect.add_tag_to_test(curId, self.reelId, scanIndex, closeChamber=True)

        self.comConnect.update_go_state()

    def remove(self):
        self.barcodesRead = self.comConnect.get_barcodes()
        tag = self.builder.get_object('scanned').get(ACTIVE)
        tags = list(self.builder.get_object('scanned').get(0, END))
        tagIndex = tags.index(tag)
        self.builder.get_object('scanned').delete(tagIndex, tagIndex)
        tags.pop(tagIndex)
        self.builder.tkvariables.get('addTag').set(tag)
        self.barcodesRead.pop(tag.split(',')[0].strip())
        self.comConnect.set_barcodes(self.barcodesRead)
        self.comConnect.open_chambers(indexes=[int(tag.split(',')[1].strip())])
        self.comConnect.update_go_state()

    def change_params_state(self, state='disabled'):
        self.builder.get_object('connect')['state'] = state
        self.builder.get_object('configs')['state'] = state
        self.builder.get_object('reelId')['state'] = state
        self.builder.get_object('test_config')['state'] = state
        self.builder.get_object('numTags')['state'] = state if state == 'disabled' else 'normal'
        self.builder.get_object('go')['state'] = state
        self.builder.get_object('add')['state'] = state
        self.builder.get_object('remove')['state'] = state
        self.builder.get_object('read_qr')['state'] = state
        self.builder.get_object('addTag')['state'] = state if state == 'disabled' else 'normal'

    def set_gui_defaults(self):
        self.builder.tkvariables.get('numTags').set(DEF_NUM_OF_TAGS)
        if self.token is None:
            self.builder.get_variable('sendToCloud').set('0')
        else:
            self.builder.get_variable('sendToCloud').set('1')
            

    def open_configs(self):
        if self.configsGui is not None and not self.configsGui.is_gui_opened():
            self.configsTtk = Toplevel(self.ttk)
            self.ttk.eval(f'tk::PlaceWindow {str(self.configsTtk)} center')
            self.configsGui.gui(self.configsTtk, self.builder)

    def test_config(self, *args):
        self.configsGui.config_set(self.builder.get_object('test_config').get())

    def open_com_ports(self):
        if self.comConnect is not None and not self.comConnect.is_gui_opened():
            self.comTtk = Toplevel(self.ttk)
            self.ttk.eval(f'tk::PlaceWindow {str(self.comTtk)} center')
            self.comConnect.gui(self.comTtk)

    def read_qr(self):
        barcode, reel = self.comConnect.read_barcode()
        # print(barcode)
        if barcode is not None:
            tagTypeObj = self.builder.tkvariables.get('tagType')
            tagTypeObj.set(barcode)
        else:
            popup_message(f'Error reading external ID, try repositioning the tag.')
        if reel is not None:
            tagTypeObj = self.builder.tkvariables.get('reelId')
            tagTypeObj.set(reel)
            self.reelId = reel
        # self.testId = (barcode[-9:])
        self.tagType = DEFAULT_CONFIG
        self.builder.get_object('test_config').set(self.tagType)
        self.configsGui.set_default_config(self.tagType)
        self.configsGui.set_params(self.tagType)
        self.change_params_state(state='enabled')

    def update_params(self):
        self.params = params = self.configsGui.get_params()
        self.runDataDict['antennaType'] = self.builder.get_object('test_config').get()
        self.dataBaseDict['timestamp'] = datetime.datetime.fromtimestamp(self.testId).strftime('%d/%m/%y %H:%M:%S')
        self.dataBaseDict['num of tags'] = self.builder.get_object('numTags').get()
        self.dataBaseDict['attenBle [db]'] = self.runDataDict['bleAttenuation'] = params['attenBle']
        self.dataBaseDict['attenLoRa [db]'] = self.runDataDict['loraAttenuation'] = params['attenLoRa']
        self.dataBaseDict['channel'] = params['channel']
        self.dataBaseDict['total time'] = params['tTotal']
        self.dataBaseDict['on time'] = params['tOn']
        self.dataBaseDict['energizing pattern'] = self.runDataDict['energizingPattern'] = params['pattern']
        self.dataBaseDict['test duration [sec]'] = self.runDataDict['testTime'] = params['testTime']
        self.dataBaseDict['reel'] = self.builder.tkvariables.get('reelId').get()
        self.dataBaseDict['GTIN'] = self.comConnect.get_GTIN()
        if 'sleep' in params.keys():
            self.sleep = int(params['sleep'])
        else:
            self.sleep = 0
        self.testTime = float(params['testTime'])

    def send_gw_commands(self):
        if self.sleep > 0:
            for i in range(self.sleep):
                sleep(1)
                if i % 3 == 0:
                    print('.', end='')
            print()
        self.gatewayDataReceive = Thread(target=self.recv_data_from_gw, args=())
        self.gatewayDataReceive.start()
        try:
            self.comConnect.send_gw_app(self.params)
        except:
            print()
        self.testFinished = False

    def recv_data_from_gw(self):
        self.packetDict = {}
        self.tagsFinished = {}
        self.testGo = True
        self.sendCommandThread.join()
        self.builder.get_object('stop')['state'] = 'enabled'
        self.startTime = self.comConnect.get_gw_time()
        lastTime = testStartTime = time.time()
        targetTime = testStartTime + self.testTime
        addToDictThreads = []
        packetsList = []
        recvDataMutex.acquire()
        while time.time() < targetTime:
            sleep(0.001)
            try:
                if self.closeRequested or not self.comConnect.is_gw_serial_open():
                    print("DataHandlerProcess Stop")
                    self.closeRequested = False
                    break

                if self.comConnect.is_gw_data_available():

                    gwData = self.comConnect.get_data()

                    if isinstance(gwData, dict):
                        gwData = [gwData]

                    for packet in gwData:
                        if 'process_packet' in packet['raw']:
                            self.packetsCount += 1
                            packetsList.append(packet)
                            curTime = time.time()
                            if curTime-lastTime > 2 and len(packetsList)>0:
                                tempThread = Thread(target=self.add_to_packet_dict, args=([packetsList.copy()]))
                                tempThread.start()
                                addToDictThreads.append(tempThread)
                                packetsList = []
                                lastTime = curTime

            except BaseException:
                print_exc()
                pass

        self.tagsCount += len(self.barcodesRead.keys())
        for thread in addToDictThreads:
            thread.join()
        recvDataMutex.release()
        if self.calib == None:
            self.builder.get_object('stop')['state'] = 'disabled'
            self.finishThread = Thread(target=self.finished, args=())
            self.finishThread.start()
        else:
            self.comConnect.cancel_gw_commands()
            self.post_process_iteration()
            self.packetsDict[self.curAtten] = {}
            self.packetsDict[self.curAtten].update(self.packetDict)
            calibMutex.release()

    def add_to_packet_dict(self, packets):
        mutex.acquire()
        for packet in packets:
            packetRaw = packet['raw'].split('(')[1].split(')')[0].strip(' "')
            preamble = packetRaw[:PREAMBLE_BYTES * NIBS_IN_BYTE]
            self.numOfPackets += 1
            if not preamble in self.packetDict.keys() and not preamble in self.badPreambles:
                curId = None
                reelId = None
                if self.token is not None:
                    curId, reelId, gtin = self.get_packet_ext_id(packet, owner=self.owner)
    
                if self.token is not None and (curId is not None or self.debugMode) and curId not in self.comConnect.get_barcodes().keys():
                    print(f'Tag with preamble {preamble} and external ID {curId} detected but not belong to the test.')
                    self.badPreambles.append(preamble)
                    mutex.release()
                    return
    
                print(f'New Tag detected with preamble: {preamble}')
    
                self.packetDict[preamble] = {}
                self.packetDict[preamble]['packets'] = []
                self.packetDict[preamble]['ttfp'] = -1
                self.packetDict[preamble]['tbp'] = -1
                self.packetDict[preamble]['ext ID'] = curId
                self.packetDict[preamble]['reel'] = reelId
                self.packetDict[preamble]['unique'] = {}
            
            if preamble in self.badPreambles:
                continue
    
            else:
                if not packetRaw[:-5] in self.packetDict[preamble]['unique'].keys():
                    self.packetDict[preamble]['unique'][packetRaw[:-5]] = []
                self.packetDict[preamble]['unique'][packetRaw[:-5]].append(packet)
                self.packetDict[preamble]['packets'].append(packet)
        
                if len(self.packetDict[preamble]['unique'][packetRaw[:-5]]) > 3:
                    self.tagsFinished[preamble] = True
        
                if len(self.tagsFinished.keys()) >= self.comConnect.get_num_of_barcode_scanners():
                    self.closeRequested = True
        mutex.release()

    def finished(self, forceFinish=False):
        self.testGo = False
        self.comConnect.add_to_test_barcodes(self.barcodesRead)
        self.comConnect.cancel_gw_commands()
        self.comConnect.open_chambers()
        avgUnique, avgTbp, avgTtfp = self.post_process_iteration()
        self.packetsDict.update(self.packetDict)

        if self.tagsCount < self.numOfTags and not forceFinish:
            self.builder.tkvariables.get('go').set(READ)
            self.builder.tkvariables.get('numTags').set(self.numOfTags - self.tagsCount)
            self.builder.get_object('go')['state'] = 'enabled'
            self.builder.get_object('add')['state'] = 'enabled'
            self.builder.get_object('remove')['state'] = 'enabled'
            self.builder.get_object('addTag')['state'] = 'normal'
            self.builder.get_object('stop')['state'] = 'enabled'
            self.builder.tkvariables.get('addTag').set('')
            if len(self.packetDict.keys()) > 0:
                popup_message(f'Average TTFP: {avgTtfp:.2f}\nAverage Unique: {avgUnique:.2f}\nAverage TBP: {avgTbp:.2f}\nReplace tags and click on "Read"', title='Message')
            else:
                avgTtfp = -1
        else:
            self.finishThread = Thread(target=self.finish_test, args=())
            self.finishThread.start()
            

    def post_process_iteration(self):
        totalNumOfUnique = 0
        avgUnique = 1
        timesList = []
        packetsList = []
        for preamble, packets in self.packetDict.items():
            for raw, data in packets['unique'].items():
                timesList = []
                packetsList = []
                tbpList = []
                sortedPackets = sorted(data, key=lambda d: d['time'])
                lastTime = 0
                # print(preamble)
                numUnique = 1
                for packet in sortedPackets:
                    packetsList.append(packet['raw'])
                    timesList.append(packet['time'])
                    curTime = float(packet['time'])
                    tbp = curTime - lastTime
                    if lastTime != 0:
                        # print(f'{tbp}')
                        numUnique += 1
                        tbpList.append(float_precision(tbp))

                    lastTime = curTime

                    if self.packetDict[preamble]['ttfp'] > curTime or self.packetDict[preamble]['ttfp'] == -1:
                        self.packetDict[preamble]['ttfp'] = curTime

                if numUnique >= 4 and self.packetDict[preamble]['tbp'] == -1:
                    if not self.comConnect.gw_tbp_version():
                        tbp = min(tbpList)
                        self.packetDict[preamble]['tbp'] = tbp
                    else:
                        tbp = estimate_diff_packet_time(packetsList, timesList)
                        if len(tbp) > 1:
                            self.packetDict[preamble]['tbp'] = min(tbp[1:]) * (10 ** (-3))

                avgUnique = ((avgUnique * totalNumOfUnique) +
                             numUnique) / (totalNumOfUnique + 1)
                numUnique = 1
                totalNumOfUnique += 1

        if self.totalNumOfUnique == 0 and totalNumOfUnique == 0:
            self.avgUnique = -1
        else:
            self.avgUnique = (((self.avgUnique * self.totalNumOfUnique) + (avgUnique * totalNumOfUnique)) / (self.totalNumOfUnique + totalNumOfUnique))
        self.totalNumOfUnique = self.totalNumOfUnique + totalNumOfUnique

        avgTbp = 0
        averageTtfp = 0
        tbpCount = 0
        count = 0
        for preamble, data in self.packetDict.items():
            count += 1
            if data['tbp'] != -1:
                tbpCount += 1
                avgTbp = ((avgTbp * (tbpCount - 1) + data['tbp']) / tbpCount)
            averageTtfp = ((averageTtfp * (count - 1)) + data['ttfp']) / count

        return avgUnique, avgTbp, averageTtfp

    def finish_test(self):
        uniqueValid = self.post_process(self.packetsDict)

        passFail = ((len(self.packetsDict.keys()) / len(self.barcodesRead.keys())) * 100) >= int(self.params['respondingMu'])
        passFail = 'Passed' if passFail else 'Failed'

        avgTtfp = self.dataBaseDict['TTFP-AVG [sec]']
        avgTbp = self.dataBaseDict['TBP-AVG [sec]'] if 'TBP-AVG [sec]' in self.dataBaseDict.keys() else -1

        
        self.files_and_cloud(uniqueValid)
        
        self.tagsCount = 0
        self.builder.tkvariables.get('numTags').set(self.numOfTags)
        self.builder.tkvariables.get('go').set(READ)
        self.comConnect.reset_test_barcodes()
        self.builder.get_object('connect')['state'] = 'enabled'
        self.builder.get_object('read_qr')['state'] = 'enabled'
        self.builder.get_object('stop')['state'] = 'enabled'
        self.builder.get_object('go')['state'] = 'disabled'
        self.testFinished = True
        popup_message(f'Test has {passFail}\nAverage TTFP: {avgTtfp}\nAverage unique packets: {self.avgUnique:.2f}\nAverage time between packets: {avgTbp}', title='Finished test')
        
    def files_and_cloud(self ,uniqueValid):
        if not isdir(OUTPUT_DIR):
            makedirs(OUTPUT_DIR)
        testDir = datetime.datetime.fromtimestamp(self.testId).strftime('%d%m%y_%H%M%S')
        mkdir(join(OUTPUT_DIR, testDir))
        
        self.runDataDict['testerStationName'] = self.stationName 
        self.runDataDict['commonRunName'] = commonRunName = self.reelId + '_' + testDir
        self.runDataDict['testerType'] = 'sample'
        self.runDataDict['gwVersion'] = self.comConnect.get_gw_version()
        
        tagsDataPath = abspath(join(OUTPUT_DIR, testDir, f'{commonRunName}@packets_data.csv'))
        packetsCsv = CsvLog(HeaderType.TAG, tagsDataPath, tester_type=TesterName.SAMPLE, new_convention=True)
        packetsCsv.open_csv()

        for preamble, data in self.packetsDict.items():
            if len(data['packets']) > 0:
                for packet in data['packets']:
                    tagRow = {'commonRunName': commonRunName,
                              'encryptedPacket': packet['raw'],
                              'time': packet['time'],
                              'externalId': data['ext ID']}
                    packetsCsv.append_dict_as_row([tagRow])
                    
        self.post_tags_data(tagsDataPath)
        
        runDataPath = abspath(join(OUTPUT_DIR, testDir, f'{commonRunName}@run_data.csv'))
        runCsv = CsvLog(HeaderType.RUN, runDataPath, tester_type=TesterName.SAMPLE)
        runCsv.open_csv()
        runCsv.append_dict_as_row([self.runDataDict])
        
        self.post_run_data(runDataPath)

        if len(uniqueValid) > 0:
            with open(join(OUTPUT_DIR, testDir, f'{commonRunName}@unique_data.csv'), 'w+', newline='') as newCsv:
                writer = csv.DictWriter(newCsv, fieldnames=uniqueValid[0].keys())
                writer.writeheader()
                writer.writerows(uniqueValid)

        with open(join(OUTPUT_DIR, testDir, f'{commonRunName}@config_data.csv'), 'w+', newline='') as newCsv:
            writer = csv.DictWriter(newCsv, fieldnames=CSV_DATABASE_COLUMNS)
            writer.writeheader()
            writer.writerows([self.dataBaseDict])

        with open(join(OUTPUT_DIR, testDir,  f'{commonRunName}@ext_ids_data.csv'), 'w+', newline='') as newCsv:
            writer = csv.DictWriter(newCsv, fieldnames=ID_CSV_COLUMNS)
            writer.writeheader()
            idsDict = self.comConnect.get_test_barcodes()
            tempDict = []
            for tagId, chamber in idsDict.items():
                tempDict.append({'ext_id': tagId, 'chamber': chamber})
            writer.writerows(tempDict)

            
    def get_packet_ext_id(self, packet, owner='wiliotmnf'):
        gtin = None
        curId = None
        reelId = None

        conn = http.client.HTTPSConnection("api.wiliot.com")

        packetTime = packet['time']
        packetRaw = packet['raw'].split('(')[1].split(')')[0].strip(' "')
        packetPayload = packetRaw[PAYLOAD_START * NIBS_IN_BYTE:]
        packetPayload = packetPayload[: CRC_START * NIBS_IN_BYTE]
        # print(packetRaw)
        # print(packetPayload)

        payload = '{\"gatewayType\":\"Manufacturing\",\"gatewayId\":\"manufacturing-gateway-id\",\"timestamp\":' + str(time.time()) + ',\"packets\":[{\"timestamp\":' + str(packetTime * (10 ** 6)) + ',\"payload\":\"' + packetPayload + '\"}]}'

        headers = {
            'accept': "application/json",
            'authorization': "Bearer " + self.token + "",
            'content-type': "application/json"
        }

        conn.request("POST", f"/v1/owner/{owner}/resolve", payload, headers)

        res = conn.getresponse()
        data = res.read()

        data = loads(data.decode("utf-8"))
        # print(data)

        if 'externalId' in data['data'][0].keys() and data['data'][0]['externalId'] != 'unknown':
            try:
                fullData = data['data'][0]['externalId']
                gtin = ')'.join(fullData.split(')')[:2]) + ')'
                tagData = fullData.split(')')[2]
                curId = tagData.split('T')[1].strip("' ")
                reelId = tagData.split('T')[0].strip("' ")
            except:
                pass
        return curId, reelId, gtin
    
    def post_tags_data(self, filePath, destination='tags-indicators'):
        self.post_data(filePath, destination)

    def post_run_data(self, filePath, destination='runs-indicators'):
        self.post_data(filePath, destination)

    def post_data(self, filePath, destination):
        if self.token is not None:
            url = f'https://api.wiliot.com/test/v1/manufacturing/upload/testerslogs/sample-test/{destination}'
            payload={}
            files=[
              ('file',(basename(filePath),open(filePath,'rb'),'text/csv'))
            ]
            headers = {
              'Authorization': f'Bearer {self.token}' 
            }
            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            print(response.text)


    def post_process(self, packetsDict):
        numOfAnswered = len(packetsDict.keys())
        self.dataBaseDict['num of packets'] = self.numOfPackets
        self.dataBaseDict['num of tags'] = self.runDataDict['tested'] = self.tagsCount
        self.dataBaseDict['tags answered'] = self.runDataDict['passed'] = numOfAnswered
        self.dataBaseDict['% responding'] = self.runDataDict['yield'] = f'{int((numOfAnswered/self.tagsCount)*100)}' + '%'

        ttfpArr = [packet['ttfp'] for packet in packetsDict.values()]
        avgTtfp = sum(ttfpArr) / numOfAnswered if numOfAnswered > 0 else -1
        ttfpArr = ttfpArr if len(ttfpArr) > 0 else [-1]
        self.dataBaseDict['TTFP-STD [sec]'] = stdTtfp = f'{numpy.std(ttfpArr):.2f}'
        self.dataBaseDict['TTFP-AVG [sec]'] = avgTtfp = f'{avgTtfp:.2f}'
        self.dataBaseDict['TTFP-Min [sec]'] = minTtfp = f'{min(ttfpArr):.2f}'
        self.dataBaseDict['TTFP-Max [sec]'] = maxTtfp = self.runDataDict['maxTtfp'] = f'{max(ttfpArr):.2f}'

        tbpArr = []
        uniqueValid = []
        for preamble, packet in packetsDict.items():
            if packet['tbp'] != -1:
                tbpArr.append(packet['tbp'])
            uniqueValid.append({'preamble': preamble, 'tbp': f"{ packet['tbp']:.2f}", 'ttfp': f"{packet['ttfp']:.2f}", 'ext ID': f"{packet['ext ID']}", 'reel': f"{packet['reel']}"})
        if len(tbpArr) > 0:
            self.dataBaseDict['TBP-STD [sec]'] = f'{numpy.std(tbpArr):.2f}'
            avgTbp = sum(tbpArr) / len(tbpArr)
            self.dataBaseDict['TBP-AVG [sec]'] = f'{avgTbp:.2f}'
            self.dataBaseDict['TBP-Min [sec]'] = f'{min(tbpArr):.2f}'
            self.dataBaseDict['TBP-Max [sec]'] = f'{max(tbpArr):.2f}'
        return uniqueValid

    def reset(self):
        if popup_yes_no():

            self.ttk.destroy()
            _exit(1)
        else:
            pass

    def close(self):
        self.ttk.destroy()
        _exit(0)
        
    def update_data(self):
        tempComs = {}
        if isfile(join('configs', '.defaults.json')):
            with open(join('configs', '.defaults.json'), 'r') as defaultComs:
                tempComs = load(defaultComs)
        if self.stationName.strip() != '':
            tempComs['stationName'] = self.stationName
        if self.owner.strip() != '':
            tempComs['owner'] = self.owner
        with open(join('configs', '.defaults.json'), 'w+') as defaultComs:
            dump(tempComs, defaultComs, indent=4)

    def popup_login(self):
        NORM_FONT = ("Helvetica", 10)
        popup = Tk()
        popup.eval('tk::PlaceWindow . center')
        popup.wm_title('Login')

        def quit_tester():
            popup.destroy()
            _exit(0)
            
        popup.protocol("WM_DELETE_WINDOW", quit_tester)
        
        def update_owner():
            owners = list(self.claimSet['owners'].keys())
            c1['values'] = owners
            c1['state'] = 'enabled'
            if 'owner' in self.defaultDict.keys() and self.defaultDict['owner'] in owners:
                defOwner = self.defaultDict['owner']
            else:
                defOwner = owners[0]
            c1.set(defOwner)
            b3['state'] = 'active'

        def login():
            print('Requesting token...')
            username = e1.get()
            password = e2.get()
            if username.strip() != '' and password.strip() != '':
                environ['FUSION_AUTH_USER'] = username
                environ['FUSION_AUTH_PASSWORD'] = password
                # print(username)
                # print(password)
            self.get_token()
            if self.token is not None:
                update_owner()
            # popup.destroy()

        def ok():
            self.owner = c1.get()
            self.stationName = e3.get()
            popup.destroy()

        if self.token is None:
            l1 = Label(popup, text='Enter FusionAuth User-Name and Password:', font=NORM_FONT)
            l1.grid(row=1, column=0, padx=10, pady=10, columnspan=3)
            l2 = Label(popup, text='Username:', font=NORM_FONT)
            l2.grid(row=2, column=0, padx=10, pady=10)
            e1 = Entry(popup)
            e1.grid(row=2, column=1, padx=10, pady=5)
            l3 = Label(popup, text='Password:', font=NORM_FONT)
            l3.grid(row=3, column=0, padx=10, pady=10)
            e2 = Entry(popup, show='*')
            e2.grid(row=3, column=1, padx=10, pady=5)
            b1 = Button(popup, text="Quit", command=quit_tester, height=1, width=10)
            b1.grid(row=4, column=0, padx=10, pady=10)
            b2 = Button(popup, text="Login", command=login, height=1, width=10)
            b2.grid(row=4, column=2, padx=10, pady=10)
        else:
            l1 = Label(popup, text='Choose owner and station name:', font=NORM_FONT)
            l1.grid(row=1, column=0, padx=10, pady=10, columnspan=3)
        l4 = Label(popup, text='Owner:', font=NORM_FONT)
        l4.grid(row=5, column=0, padx=10, pady=10)
        c1 = ttk.Combobox(popup, state='disabled')
        c1.grid(row=5, column=1, padx=10, pady=15)
        l5 = Label(popup, text='Station Name:', font=NORM_FONT)
        l5.grid(row=6, column=0, padx=10, pady=10)
        e3 = Entry(popup)
        if 'stationName' in self.defaultDict.keys():
            e3.insert(0, self.defaultDict['stationName'])
        e3.grid(row=6, column=1, padx=10, pady=5)
        b3 = Button(popup, text="OK", command=ok, height=1, width=10)
        b3.grid(row=7, column=1, padx=10, pady=10)
        
        if self.claimSet is not None:
            update_owner()
        
        popup.mainloop()
        
    def get_token(self):
        try:
            username = environ.get('FUSION_AUTH_USER')
            username = quote(username)
            password = environ.get('FUSION_AUTH_PASSWORD')
            password = quote(password)
            conn = http.client.HTTPSConnection("api.wiliot.com")
            headers = {'accept': "application/json"}
            conn.request("POST", "/v1/auth/token?password=" + password + "&username=" + username, headers=headers)
            res = conn.getresponse()
            data = res.read()
            tokens = loads(data.decode("utf-8"))
            # print(tokens)
            self.token = token = tokens['access_token']
            self.claimSet = jwt.decode(token, options={"verify_signature": False})
            self.save_token(tokens)
            print('Token received successfully.')
            # print(token)
        except:
            # print_exc()
            self.token = None
            print('Could not generate token, check username and password.')
            token = None
        return token
        
    def check_token(self):
        if isfile(join('configs', TOKEN_FILE_NANE)):
            f = open(join('configs', TOKEN_FILE_NANE), "rb")
            token = pickle.load(f)
            f.close()
            if (datetime.datetime.now() - token['issue_date']).days < 1 and (datetime.datetime.now() - token['issue_date']).seconds < 6*60*60:
                self.token = token['access_token']
                self.claimSet = jwt.decode(token['access_token'], options={"verify_signature": False})
                print('Token loaded successfully.')
            elif (datetime.datetime.now() - token['issue_date']).days < 7:
                self.refresh_token(token['refresh_token'])
    
    def refresh_token(self, refreshToken):
        try:
            conn = http.client.HTTPSConnection("api.wiliot.com")
            headers = {'accept': "application/json"}
            conn.request("POST", "/v1/auth/refresh?refresh_token=" + refreshToken, headers=headers)
            res = conn.getresponse()
            data = res.read()
            tokens = loads(data.decode("utf-8"))
            self.save_token(tokens)
            # print(tokens)
            self.token = token = tokens['access_token']
            self.claimSet = jwt.decode(token, options={"verify_signature": False})
            print('Token refreshed successfully.')
            # print(token)
        except:
            # print_exc()
            self.token = None
            print('Could not refresh token.')
            token = None
        return token
    
    def save_token(self, token):
        token['issue_date'] = datetime.datetime.now()
        pickle.dump(token, open(join('configs', TOKEN_FILE_NANE), "wb"))


def popup_yes_no():
    root = Tk()
    root.wm_withdraw()
    result = messagebox.askquestion("Sample Test", "Reset Sample Test?", icon='warning')
    root.destroy()
    if result == 'yes':
        return True
    else:
        return False


def float_precision(num, prec=2):
    dotPos = str(num).index('.')
    firstIdx = [i for i in range(len(str(num))) if str(num)[i] != '0' and str(num)[i] != '.']
    firstIdx = firstIdx[0] if firstIdx[0] > 0 else firstIdx[0] + 1
    afterDot = firstIdx - dotPos + prec
    if afterDot > 0:
        evalStr = '{:.%sf}' % (str(firstIdx - dotPos + prec))
    else:
        evalStr = '{:.0f}'
    return float(evalStr.format(num))


if __name__ == '__main__':
    calib = None
    low = None
    high = None
    step = None

    parser = argparse.ArgumentParser(description='Run PixieParser')
    parser.add_argument('-d', '--debug', action='store_true' , default='False', help='Debug mode')
    parser.add_argument('-c', '--calib' , help='Calibration mode, attenuator type')
    parser.add_argument('-low', '--low', help='lower value of attenuation')
    parser.add_argument('-high', '--high', help='higher value of attenuation')
    parser.add_argument('-step', '--step', help='attenuation step')
    args = parser.parse_args()
    if args.debug is not None:
        debugMode = args.debug
    if args.calib is not None and args.low is not None and args.high is not None and  args.step is not None:
        calib = args.calib
        low = args.low
        high = args.high
        step = args.step
    elif args.calib is not None:
        print('Warning - Missing values for calibration mode.')
    # Run the UI
    app_folder = abspath(join(dirname(__file__), '..'))
    try:
        sampleTest = SampleTest(debugMode=debugMode, calib=calib, low=low, high=high, step=step)
        sampleTest.gui()
    except BaseException:
        print_exc()
    exit(0)
