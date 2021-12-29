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
     nor are you named on the U.S. Treasury Department’s list of Specially Designated
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
Created on Oct 31, 2021

@author: davidd
'''
import serial
import threading
from time import sleep, time
from tkinter import *
from serial import tools
import pygubu
from sys import path
from os.path import abspath, dirname, join, isfile
from json import load, dump
path.append(abspath(dirname(join('..', '..', '..', '..', 'pywiliot_internal'))))
from pywiliot_internal.wiliot.wiliot_testers.test_equipment import *
from pywiliot_internal.wiliot.gateway_api.gateway import WiliotGateway, ActionType, DataType

path.append(abspath(join(dirname(__file__), '..', '..', '..', '..', 'wiliot-debug-jtag-tool')))

mutex = threading.Lock()
barcodeMutex = threading.Lock()

CONNECT_HW = 'Connect HW'
GO = 'Go'
CONTINUE = 'Continue'
READ = 'Read'

ADD = 'ADD'
REMOVE = 'REMOVE'

GW_CANCEL = '!reset'

# gateway
GW_RESET = '!reset'
GW_VERSION = 'Gateway version: '
GW_AVAILABLE_VERSION = 'Available Version: '
GW_PARAMETERS = ['tTotal', 'tOn', 'channel', 'pattern', 'attenuation']

GW_APP = '!gateway_app'
GW_APP_ETC = '2480 0 2402'
GW_APP_PARAMS = {'prefix': GW_APP, 'channel': '',
                 'tTotal': '', 'tOn': '', 'etc': GW_APP_ETC}

GW_ENERGIZING = '!set_energizing_pattern'
GW_ENERGIZING_PARAMS = {'prefix': GW_ENERGIZING, 'pattern': ''}

# attenuator
ATTENUATION = 'atten'

BLE = 'Ble'
LORA = 'LoRa'

BARCODES = 'Barcodes'
ATTENUATORS = 'Atten'
CHAMBERS = 'Chambers'

GW_TBP_VERSION = '2.5.1'


class ComConnect(object):
    '''
    classdocs
    '''
    isGui = False
    hwConnected = False
    gwTbpVersion = False
    gateway = None
    attenuator = None
    chambersMoveCom = ''
    barcodesMoveCom = ''
    barcodesState = ADD
    chambersState = ADD
    barcodesSerials = {}
    chambersSerials = {}
    attenSerials = {}
    testBarcodes = {}
    barcodesRead = {}
    usedPorts = []
    gwComPort = []
    gwUpdateStatus = 'disabled'
    gwVersion = ''
    startTime = 0

    def __init__(self, topBuilder=None):
        '''
        Constructor
        '''
        self.gateway = WiliotGateway()
        self.topBuilder = topBuilder
        # self.chamber = Tescom('COM3')

    def __del__(self):
        if self.gateway is not None and self.is_gw_serial_open():
            self.gateway.close_port()

        for comPort, barcode in self.barcodesSerials.items():
            if barcode is not None and barcode.is_open():
                barcode.close_port()

        for comPort, chamber in self.chambersSerials.items():
            if chamber is not None and chamber.is_connected():
                chamber.open_chamber()
                chamber.close_port()

        # for comPort, atten in self.attenSerials.items():
        #     if atten!=None and 'serial' in atten.keys() and atten['serial']!=None and atten:
        #         atten.disconnect()

    def gui(self, ttkFrame=None):
        self.builder = builder = pygubu.Builder()
        uifile = join(abspath(dirname(__file__)), 'utils', 'com_connect.ui')
        self.builder.add_from_file(uifile)

        imgPath = join(abspath(dirname(__file__)), '.')
        builder.add_resource_path(imgPath)
        imgPath = join(abspath(dirname(__file__)), 'utils')
        builder.add_resource_path(imgPath)

        self.ttk = ttkFrame

        self.ttk.title("ComConnect")

        self.mainwindow = self.builder.get_object('mainwindow', self.ttk)

        self.ttk = self.ttk

        self.builder.connect_callbacks(self)
        self.set_gui_defaults()
        self.find_com_ports()

        self.ttk.protocol("WM_DELETE_WINDOW", self.close)
        self.ttk.lift()
        self.ttk.attributes("-topmost", True)
        self.ttk.attributes("-topmost", False)

        # self.set_gui_defaults()

        self.isGui = True
        self.ttk.mainloop()

    def set_gui_defaults(self):
        if self.serials_connected(BARCODES):
            self.builder.get_object('connect_barcodes').configure(text='Disconnect')
        else:
            self.builder.get_object('connect_barcodes').configure(text='Connect')

        if self.serials_connected(CHAMBERS):
            self.builder.get_object('connect_chambers').configure(text='Disconnect')
        else:
            self.builder.get_object('connect_chambers').configure(text='Connect')

        if len(self.gwComPort)>0:
            self.builder.get_object('gwCom').set(self.gwComPort[0])
        if self.is_gw_serial_open():
            self.builder.get_object('connect_gw').configure(text='Disconnect')
            self.builder.get_object('gwCom')['state'] = 'disabled'
            self.builder.get_object('version').configure(text=GW_VERSION + self.gwVersion[0])
            self.builder.get_object('latestVersion').configure(text=GW_AVAILABLE_VERSION + self.gwLatestVersion[0])
            self.builder.get_object('update_gw')['state'] = self.gwUpdateStatus
        else:
            self.builder.get_object('connect_gw').configure(text='Connect')

        bleAtten = ''
        loraAtten = ''
        for comPort, atten in self.attenSerials.items():
            bleAtten = comPort if atten['type'] == BLE else bleAtten
            loraAtten = comPort if atten['type'] == LORA else loraAtten

        self.builder.get_object('attenComBle').set(bleAtten)
        self.builder.get_object('attenComLoRa').set(loraAtten)
        if self.serials_connected(ATTENUATORS):
            self.builder.get_object('connect_atten').configure(text='Disconnect')
            self.builder.get_object('attenComBle')['state'] = 'disabled'
            self.builder.get_object('attenComLoRa')['state'] = 'disabled'
        else:
            self.builder.get_object('connect_atten').configure(text='Connect')
        pass

    def connect_all(self, gui=True):
        if not self.is_gw_serial_open():
            success = self.connect_gw(gui)
            if not success:
                return
        if not self.serials_connected(ATTENUATORS):
            self.connect_atten(gui)
        if not self.serials_connected(BARCODES):
            self.connect_barcodes(gui)
        if not self.serials_connected(CHAMBERS):
            self.connect_chambers(gui)
        self.hwConnected = True
        self.topBuilder.get_object('read_qr')['state'] = 'enabled'
        self.topBuilder.tkvariables.get('go').set(READ)
        self.topBuilder.get_object('go')['state'] = 'disabled'

    def close(self):
        if self.is_gw_serial_open() and self.serials_connected(ATTENUATORS) and self.serials_connected(BARCODES) and self.serials_connected(CHAMBERS):
            self.hwConnected = True
            self.enable_hw_connected()
        self.isGui = False
        self.ttk.destroy()

    def save(self):
        defaultDict = {}
        if isfile(join('configs', '.defaults.json')):
            with open(join('configs', '.defaults.json'), 'r') as defaultComs:
                defaultDict = load(defaultComs)
        defaultDict['gw'] = self.gwComPort[0]
        defaultDict['atten'] = {}
        for comPort, atten in self.attenSerials.items():
            defaultDict['atten'][atten['type']] = comPort
        defaultDict['barcodes'] = list(self.barcodesSerials.keys())
        defaultDict['chambers'] = list(self.chambersSerials.keys())
        with open(join('configs', '.defaults.json'), 'w+') as defaultComs:
            dump(dict(defaultDict), defaultComs, indent=4)

    def focus_bacode_available(self, *args):
        self.focus_available(BARCODES)

    def focus_bacode_chosen(self, *args):
        self.focus_chosen(BARCODES)

    def focus_chamber_available(self, *args):
        self.focus_available(CHAMBERS)

    def focus_chamber_chosen(self, *args):
        self.focus_chosen(CHAMBERS)

    def focus_available(self, obj):
        self.builder.get_object(f'add{obj}').configure(text='>')
        setattr(self, f'{obj.lower()}State', ADD)

    def focus_chosen(self, obj):
        self.builder.get_object(f'add{obj}').configure(text='<')
        setattr(self, f'{obj.lower()}State', REMOVE)
        setattr(self, f'{obj.lower()}MoveCom', '')

    def add_barcode(self):
        if getattr(self, f'{BARCODES.lower()}State') == ADD:
            comChosen = self.builder.get_object(f'available{BARCODES}').get(ACTIVE)
            tempBarcode = BarcodeScanner()
            isBarScan = tempBarcode.check_com_port(comChosen)
            if not isBarScan:
                popup_message(f'{comChosen} is not barcode scanner', title='Error')
        self.add(BARCODES)

    def add_chamber(self):
        self.add(CHAMBERS)

    def add(self, obj):
        if getattr(self, f'{obj.lower()}State') == ADD:
            sending = self.builder.get_object(f'available{obj}')
            receiving = self.builder.get_object(f'chosen{obj}')
        else:
            sending = self.builder.get_object(f'chosen{obj}')
            receiving = self.builder.get_object(f'available{obj}')

        comList = list(sending.get(0, END))
        comChosen = sending.get(ACTIVE)
        receiving.insert(END, comChosen)
        comIndex = comList.index(comChosen)
        sending.delete(comIndex, comIndex)

        newSerials = {}
        serials = getattr(self, f'{obj.lower()}Serials')
        for comPort in list(self.builder.get_object(f'chosen{obj}').get(0, END)):
            newSerials[comPort] = serials[comPort] if serials.get(
                comPort) else None
            serials.pop(comPort, None)

        for comPort, serial in serials.items():
            if serial is not None:
                if 'chamber' in obj.lower():
                    serial.open_chamber()
                    serial.close_port()
                if 'barcode' in obj.lower():
                    serial.close_port()
                self.usedPorts.pop(self.usedPorts.index(comPort))

        setattr(self, f'{obj.lower()}Serials', newSerials)

        isConnected = self.serials_connected(obj)
        if isConnected:
            self.builder.get_object(f'connect_{obj.lower()}').configure(text='Disconnect')
        else:
            self.builder.get_object(f'connect_{obj.lower()}').configure(text='Connect')

    def chamber_up(self):
        self.up(CHAMBERS)

    def chamber_down(self):
        self.down(CHAMBERS)

    def barcode_up(self):
        self.up(BARCODES)

    def barcode_down(self):
        self.down(BARCODES)

    def up(self, obj):
        comList = list(self.builder.get_object(f'chosen{obj}').get(0, END))
        if getattr(self, f'{obj.lower()}MoveCom') == '':
            chosenCom = self.builder.get_object(f'chosen{obj}').get(ACTIVE)
            setattr(self, f'{obj.lower()}MoveCom', chosenCom)
        else:
            chosenCom = getattr(self, f'{obj.lower()}MoveCom')
        comIndex = comList.index(chosenCom)
        if comIndex > 0:
            comList.pop(comList.index(chosenCom))
            comList.insert(comIndex - 1, chosenCom)
            self.builder.get_object(f'chosen{obj}').delete(0, END)
            for com in comList:
                self.builder.get_object(f'chosen{obj}').insert(END, com)
            self.builder.get_object(f'chosen{obj}').select_set(comIndex - 1)

    def down(self, obj):
        comList = list(self.builder.get_object(f'chosen{obj}').get(0, END))
        if getattr(self, f'{obj.lower()}MoveCom') == '':
            chosenCom = self.builder.get_object(f'chosen{obj}').get(ACTIVE)
            setattr(self, f'{obj.lower()}MoveCom', chosenCom)
        else:
            chosenCom = getattr(self, f'{obj.lower()}MoveCom')
        comIndex = comList.index(chosenCom)
        if comIndex < (len(comList) - 1):
            comList.pop(comList.index(chosenCom))
            comList.insert(comIndex + 1, chosenCom)
            self.builder.get_object(f'chosen{obj}').delete(0, END)
            for com in comList:
                self.builder.get_object(f'chosen{obj}').insert(END, com)
            self.builder.get_object(f'chosen{obj}').select_set(comIndex + 1)

    def find_com_ports(self, *args):
        self.comPorts = comPorts = [s.device for s in tools.list_ports.comports()]
        if len(comPorts) == 0:
            self.comPorts = comPorts = [s.name for s in tools.list_ports.comports()]

        self.availablePorts = availablePorts = [comPort for comPort in comPorts if comPort not in self.usedPorts]

        self.builder.get_object('gwCom')['values'] = availablePorts
        self.builder.get_object('attenComBle')['values'] = availablePorts + ['']
        self.builder.get_object('attenComLoRa')['values'] = availablePorts + ['']

        self.missingComPort = False
        self.update_multi_serials(availablePorts, BARCODES)
        self.update_multi_serials(availablePorts, CHAMBERS)
        self.check_chosen_ports()

        # if self.missingComPort:
        #     popup_message('Default com ports not available, check connections.', title='Warning')
        # self.set_gui_defaults()

    def check_chosen_ports(self):
        if len(self.gwComPort)>0:
            self.gwComPort[0] = self.builder.get_object('gwCom').get()
            if self.gwComPort[0] not in self.comPorts:
                self.gwComPort[0] = ''
                self.builder.get_object('gwCom').set('')
                self.missingComPort = True
        i = 0
        while i < len(self.attenSerials.keys()):
            port = list(self.attenSerials.keys())[i]
            atten = list(self.attenSerials.values())[i]
            if port != '' and port not in self.comPorts:
                self.attenSerials.pop(port)
                self.builder.get_object(f"attenCom{atten['type']}").set('')
                self.missingComPort = True
                continue
            i += 1

    def update_multi_serials(self, availablePorts, obj):
        self.builder.get_object(f'available{obj}').delete(0, END)
        self.builder.get_object(f'chosen{obj}').delete(0, END)
        ports = getattr(self, f'{obj.lower()}Serials')
        for port in availablePorts:
            if port not in ports.keys():
                self.builder.get_object(f'available{obj}').insert(END, port)
        for port in ports.keys():
            if port in self.comPorts:
                self.builder.get_object(f'chosen{obj}').insert(END, port)
            else:
                self.missingComPort = True

    def choose_com_ports(self, defaultDict):

        self.missingComPort = False

        availablePorts = [s.device for s in tools.list_ports.comports()]
        if len(availablePorts) == 0:
            availablePorts = [s.name for s in tools.list_ports.comports()]
        if 'gw' in defaultDict.keys() and defaultDict['gw'] in availablePorts:
            self.gwComPort = [defaultDict['gw']]
        else:
            self.gwComPort = ['']
            self.missingComPort = True
        if 'atten' in defaultDict.keys() and BLE in defaultDict['atten'].keys() and defaultDict['atten'][BLE] in availablePorts:
            self.attenSerials[defaultDict['atten'][BLE]] = {}
            self.attenSerials[defaultDict['atten'][BLE]]['type'] = BLE
            self.attenSerials[defaultDict['atten'][BLE]]['serial'] = None
        elif 'atten' in defaultDict.keys() and BLE in defaultDict['atten'].keys() and defaultDict['atten'][BLE].strip() != '':
            self.missingComPort = True
        if 'atten' in defaultDict.keys() and LORA in defaultDict['atten'].keys() and defaultDict['atten'][LORA] in availablePorts:
            self.attenSerials[defaultDict['atten'][LORA]] = {}
            self.attenSerials[defaultDict['atten'][LORA]]['type'] = LORA
            self.attenSerials[defaultDict['atten'][LORA]]['serial'] = None
        elif 'atten' in defaultDict.keys() and LORA in defaultDict['atten'].keys() and defaultDict['atten'][LORA].strip() != '':
            self.missingComPort = True

        if 'barcodes' in defaultDict.keys():
            self.barcodesSerials = dict.fromkeys([barcode for barcode in defaultDict['barcodes'] if barcode in availablePorts], None)
        if 'chambers' in defaultDict.keys():
            self.chambersSerials = dict.fromkeys([chamber for chamber in defaultDict['chambers'] if chamber in availablePorts], None)

        missingBarcodes = [barcode for barcode in defaultDict['barcodes'] if barcode not in availablePorts]
        missingChambers = [chamber for chamber in defaultDict['chambers'] if chamber not in availablePorts]
        if any(missingBarcodes + missingChambers):
            self.missingComPort = True

        return self.missingComPort

    def gw_port_chosen(self, *args):
        self.gwComPort = [self.builder.get_object('gwCom').get()]

    def connect_and_close(self):
        self.connect_all()
        self.close()

    def choose_ble_atten(self, *args):
        bleCom = self.builder.get_object('attenComBle').get()
        if bleCom.strip() != '':
            self.attenSerials[bleCom] = {}
            self.attenSerials[bleCom]['type'] = BLE
            self.attenSerials[bleCom]['serial'] = None

    def choose_lora_atten(self, *args):
        loraCom = self.builder.get_object('attenComLoRa').get()
        if loraCom.strip() != '':
            self.attenSerials[loraCom] = {}
            self.attenSerials[loraCom]['type'] = LORA
            self.attenSerials[loraCom]['serial'] = None

    def connect_gw(self, gui=True):
        if not self.is_gw_serial_open():
            if len(self.gwComPort)==0 or self.gwComPort[0].strip() == '':
                popup_message('No default com port for GW, please choose GW com port.', title='Error')
                return False
            comPort = self.gwComPort[0]
            self.gateway.open_port(port=comPort, baud=921600)
            # print([comSer.serial_number for comSer in serial.tools.list_ports.comports()])
            if self.is_gw_serial_open():
                print(f'GW is connected on port: {comPort}.')
                self.gateway.write(GW_RESET)
                self.usedPorts.append(comPort)
                version = self.gateway.get_gw_version()
                numeric_filter = filter(str.isdigit, version[0])
                version = [".".join(numeric_filter)]
                self.gwVersion = version
                self.gwLatestVersion = latestVersion = self.gateway.get_latest_version_number()
                curVersion = int(version[0].replace('.', ''))
                self.gwUpdateStatus = 'enabled' if curVersion < int(latestVersion[0].replace('.', '')) else 'disabled'
                if gui:
                    self.builder.get_object('update_gw')['state'] = self.gwUpdateStatus
                    self.builder.get_object('connect_gw').configure(text='Disconnect')
                    self.builder.get_object('version').configure(text=GW_VERSION + version[0])
                    self.builder.get_object('latestVersion').configure(text=GW_AVAILABLE_VERSION + latestVersion[0])
                    self.builder.get_object('gwCom')['state'] = 'disabled'
                if curVersion >= int(GW_TBP_VERSION.replace('.', '')):
                    self.gwTbpVersion = True
        else:
            self.usedPorts.remove(self.gwComPort[0])
            self.gateway.close_port()
            self.builder.get_object('connect_gw').configure(text='Connect')
            self.builder.get_object('version').configure(text=GW_VERSION)
            self.builder.get_object('latestVersion').configure(text=GW_AVAILABLE_VERSION)
            self.builder.get_object('gwCom')['state'] = 'enabled'
        if gui:
            self.find_com_ports()
            
        return True

    def connect_barcodes(self, gui=True):
        self.connect_multi_serials(BARCODES, gui=gui)

    def connect_chambers(self, gui=True):
        self.connect_multi_serials(CHAMBERS, gui=gui)

    def connect_atten(self, gui=True):
        isConnected = self.connect_multi_serials(ATTENUATORS, gui=gui)
        if gui:
            attenState = 'disabled' if isConnected else 'enabled'
            self.builder.get_object('attenComLoRa')['state'] = attenState
            self.builder.get_object('attenComBle')['state'] = attenState

    def connect_multi_serials(self, obj, gui=True):
        serials = getattr(self, f'{obj.lower()}Serials')
        isConnected = True
        if self.serials_connected(obj):
            self.close_serials(obj, serials)
            self.builder.get_object(f'connect_{obj.lower()}').configure(text='Connect')
            isConnected = False
        elif len(serials.keys()) > 0:
            self.open_serials(obj, serials)
            if gui:
                self.builder.get_object(f'connect_{obj.lower()}').configure(text='Disconnect')
        if gui:
            self.find_com_ports()
        # self.update_go_state()
        return isConnected

    def open_serials(self, obj, serials):
        for comPort, serial in serials.items():
            if 'barcode' in obj.lower():
                if serial is not None and serial.is_open():
                    continue
                serial = BarcodeScanner(com=comPort, log_type='LOG_NL')
                if serial.is_open():
                    self.usedPorts.append(comPort)
                    serials[comPort] = serial
            elif 'chamber' in obj.lower():
                if serial is not None and serial.is_connected():
                    continue
                serial = Tescom(comPort)
                if serial.is_connected():
                    self.usedPorts.append(comPort)
                    serials[comPort] = serial
                    if not serial.is_door_open():
                        serial.open_chamber()
            elif 'atten' in obj.lower():
                if serial['serial'] is not None or comPort.strip() == '':
                    # if serial['serial']!=None and
                    # serial['serial'].GetActiveTE().s.is_open():
                    continue
                serial = Attenuator('API', comport=comPort)
                # if serial.GetActiveTE().s.is_open():
                self.usedPorts.append(comPort)
                serials[comPort]['serial'] = serial

    def close_serials(self, obj, serials):
        if 'atten' in obj.lower():
            for comPort in serials.keys():
                # serial['serial'].GetActiveTE.s.close_port()
                serials[comPort]['serial'] = None
                self.usedPorts.remove(comPort)
        else:
            while len(serials.keys()) > 0:
                comPort = list(serials.keys())[0]
                serial = serials[comPort]
                if 'chamber' in obj.lower():
                    serial.open_chamber()
                serial.close_port()
                self.usedPorts.remove(comPort)
                serials.pop(comPort)

    def serials_connected(self, obj):
        serials = getattr(self, f'{obj.lower()}Serials')
        if 'atten' in obj.lower():
            serials = dict(zip(serials.keys(), [atten['serial'] for atten in serials.values()]))
        connectedSerials = 0
        for comPort, serial in serials.items():
            if serial is not None:
                if 'barcode' in obj.lower() and serial.is_open():
                    connectedSerials += 1
                if 'chamber' in obj.lower() and serial.is_connected():
                    connectedSerials += 1
                if 'atten' in obj.lower():
                    connectedSerials += 1
            # if comPort.strip()=='':
            #     connectedSerials += 1
        if connectedSerials > 0 and connectedSerials == len(serials.keys()):
            return True
        else:
            return False
        print('Error')

    def get_data(self, actionType=ActionType.CURRENT_SAMPLES, numOfPackets=1, dataType=DataType.RAW):
        return self.gateway.get_data(action_type=actionType, num_of_packets=numOfPackets, data_type=dataType)

    def read_barcode(self, scannerIndex=0, closeChamber=False):
        scanner = list(self.barcodesSerials.values())[scannerIndex]
        curId, reelId, gtin = scanner.scan_ext_id(scanDur=5)
        self.curId = curId
        # self.reelId = reelId
        self.gtin = gtin
        if curId is None:
            barcodeMutex.acquire()
            if closeChamber:
                self.barcodeError.append(scannerIndex)
            barcodeMutex.release()
            # print(f'Error reading external ID (chamber {scannerIndex}), try repositioning the tag.')
            # popup_message(f'Error reading external ID (chamber {scannerIndex}), try repositioning the tag.')
            return None, None

        if not closeChamber:
            reelIdObj = self.topBuilder.tkvariables.get('reelId')
            reelIdObj.set(reelId)
            self.reelId = reelId

        else:
            self.add_tag_to_test(curId, reelId, scannerIndex, closeChamber)

        return curId, reelId

    def add_tag_to_test(self, curId, reelId, scannerIndex=0, closeChamber=False):
        mutex.acquire()
        if curId not in self.testBarcodes.keys() and curId not in self.barcodesRead.keys() and closeChamber:
            self.barcodesRead[curId] = scannerIndex
            # self.testBarcodes[curId] = scannerIndex
            self.topBuilder.get_object('scanned').insert(END, f'{curId}, {scannerIndex}')
            mutex.release()
            chambers = list(self.chambersSerials.values())
            if len(chambers) > scannerIndex and chambers[scannerIndex] is not None:
                chambers[scannerIndex].close_chamber()
        elif closeChamber:
            mutex.release()
            popup_message(f'Tag {curId} already read.')
        else:
            mutex.release()

        if self.reelId != '' and self.reelId != reelId:
            popup_message('Tag reel different from test reel.', title='Warning')

    def read_scanners_barcodes(self, indexes=[]):
        if len(indexes) == 0:
            self.barcodesRead = {}
            self.topBuilder.get_object('scanned').delete(0, END)
            indexes = list(range(len(self.barcodesSerials.values())))
        scannerThreads = []
        self.barcodeError = []

        popupThread = threading.Thread(target=popup_message, args=('Chambers are closing!!\nWatch your hands!!!', 'Warning', ("Helvetica", 18)))
        popupThread.start()
        popupThread.join()

        for i in indexes:
            t = threading.Thread(target=self.read_barcode, args=(i, True))
            scannerThreads.append(t)
            t.start()
        for i in range(len(scannerThreads)):
            t = scannerThreads[i]
            t.join()

        self.update_go_state()
        self.topBuilder.get_object('add')['state'] = 'enabled'
        self.topBuilder.get_object('remove')['state'] = 'enabled'
        self.topBuilder.get_object('addTag')['state'] = 'normal'
        self.topBuilder.get_object('go')['state'] = 'enabled'
        if len(self.barcodeError) > 0:
            popup_message(f'Error reading external ID from chambers {self.barcodeError}, try repositioning the tags.')

    def enable_hw_connected(self):
        self.topBuilder.get_object('read_qr')['state'] = 'enabled'
        if self.topBuilder.tkvariables.get('go').get() == CONNECT_HW:
            self.topBuilder.tkvariables.get('go').set(READ)
            self.topBuilder.get_object('go')['state'] = 'disabled'

    def update_go_state(self):
        if len(self.barcodesSerials) == len(self.barcodesRead.keys()) and len(self.testBarcodes.keys()) > 0:
            self.topBuilder.tkvariables.get('go').set(CONTINUE)
        elif len(self.barcodesSerials) == len(self.barcodesRead.keys()):
            self.topBuilder.tkvariables.get('go').set(GO)
        else:
            self.topBuilder.tkvariables.get('go').set(READ)
        # self.topBuilder.get_object('go')['state'] = 'enabled'

    def send_gw_app(self, params):
        # curBarcodes = list(self.topBuilder.get_object('scanned').get(0, END))
        # self.testBarcodes.update(curBarcodes)
        tempGwParams = GW_APP_PARAMS
        tempGwEnergizing = GW_ENERGIZING_PARAMS
        for param, value in params.items():
            if tempGwEnergizing.get(param) is not None:
                tempGwEnergizing[param] = value
            if tempGwParams.get(param) is not None:
                tempGwParams[param] = value
            if param.startswith(ATTENUATION):
                for comPort, atten in self.attenSerials.items():
                    if param.lower().endswith(atten['type'].lower()):
                        # atten['serial'].GetActiveTE().Setattn(int(value))
                        attenuation = atten['serial'].GetActiveTE().Setattn(float(value))
                        print(f"{atten['type']} Attenuation set to: {str(attenuation).strip()}")

        self.gateway.write(b'!set_packet_filter_off')
        sleep(0.1)
        self.gateway.write(b'!set_pacer_interval 0')
        sleep(0.1)
        if self.gwTbpVersion:
            print('TBP calculation using GW time.')
            testerModeCommand = b'!set_tester_mode 1'
            self.gateway.write(testerModeCommand)
            print(testerModeCommand)
            sleep(0.1)

        gwEnerCommand = ' '.join(list(tempGwEnergizing.values()))
        self.gateway.write(gwEnerCommand)
        print(gwEnerCommand)

        sleep(0.1)

        gwAppCommand = ' '.join(list(tempGwParams.values()))
        self.gateway.write(gwAppCommand)
        print(gwAppCommand)

        self.startTime = time()
        self.gateway.run_packets_listener(do_process=True, tag_packets_only=False)

    def get_barcodes(self):
        return self.barcodesRead

    def get_reel_ID(self):
        return self.reelId

    def get_GTIN(self):
        return self.gtin

    def get_test_barcodes(self):
        return self.testBarcodes

    def is_gw_serial_open(self):
        serialOpen, _, _ = self.gateway.get_connection_status()
        return serialOpen

    def is_gw_data_available(self):
        return self.gateway.is_data_available()

    def is_gui_opened(self):
        return self.isGui

    def get_gw_version(self):
        return self.gwVersion[0]

    def update_gw(self):
        self.gateway.update_version()

    def get_gw_time(self):
        return self.startTime

    def add_to_test_barcodes(self, barcodes):
        self.testBarcodes.update(barcodes)

    def set_barcodes(self, barcodes):
        self.barcodesRead = barcodes

    def cancel_gw_commands(self):
        self.gateway.stop_processes()
        self.gateway.write(GW_CANCEL)
        sleep(0.1)

    def is_hw_connected(self):
        return self.hwConnected

    def reset_test_barcodes(self):
        self.testBarcodes = {}
        # self.barcodesRead = {}

    def open_chambers(self, indexes=[]):
        chambers = list(self.chambersSerials.values())
        if len(indexes) == 0:
            indexes = list(range(len(chambers)))
        for index in indexes:
            if len(chambers) > index and chambers[index] is not None:
                chambers[index].open_chamber()
                
    def close_chambers(self, indexes=[]):
        chambers = list(self.chambersSerials.values())
        if len(indexes) == 0:
            indexes = list(range(len(chambers)))
        for index in indexes:
            if len(chambers) > index and chambers[index] is not None:
                chambers[index].close_chamber()

    def get_num_of_barcode_scanners(self):
        return len(self.barcodesSerials.keys())

    def get_error_barcode(self):
        self.barcodeError

    def gw_tbp_version(self):
        return self.gwTbpVersion


def popup_message(msg, title='Error', font=("Helvetica", 10)):
    popup = Tk()
    popup.eval('tk::PlaceWindow . center')
    popup.wm_title(title)
    print(f'{title} - {msg}')

    def popup_exit():
        popup.destroy()

    label = Label(popup, text=msg, font=font)
    label.pack(side="top", fill="x", padx=10, pady=10)
    B1 = Button(popup, text="Okay", command=popup_exit)
    B1.pack(padx=10, pady=10)
    popup.mainloop()
