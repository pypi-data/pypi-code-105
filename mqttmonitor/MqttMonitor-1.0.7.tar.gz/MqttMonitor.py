#
# Copyright (c) 2021 Fw-Box (https://fw-box.com)
# Author: Hartman Hsieh
#
# Description :
#   The function is based on MQTT.
#   When the original serial of ESP8266/ESP32 cannot be used,
#   it can replace serial print.
#
# Libraries :
#    pip install paho.mqtt
#

from tkinter import *
from tkinter import ttk
import tkinter.font as Font
import threading
import time
import paho.mqtt.client as mqtt
import json
from io import StringIO
import random, string
import queue
import threading
from tkinter import filedialog
#from tkinter import messagebox
from datetime import datetime
import webbrowser


__version__ = "1.0.7"


MainWin = Tk()


WIN_BG = "white"
WIDGET_BG = "white"
WIDGET_FG = "black"
PAD_X = 10
PAD_Y = 10
IPAD_X = 0
IPAD_Y = 0

STATUS_STR_CONNECTED = "O"
STATUS_STR_DISCONNECTED = "X"

gLabelMessage = None
TextInfo = None
gLabelStatus = None
gVarCheckAutoscroll = None
gVarCheckSaveLog = None
gButtonRun = None
gClient = None
gSubTopic = ""
gMqttRunning = False
gAppConfig = None
gQueueForFile = None
gWinSettings = None
gFont = Font.Font(size = 10, weight = 'bold')
gStartSavingLog = False
gFileWriteThread = None
gLogFileName = ""
#gMqttSettingIndex = 0
gMqttSetting = None
    
def main():
    global gQueueForFile
    global gAppConfig
    global gMqttSetting
    global TextInfo
    global MainWin

    gQueueForFile = queue.Queue(10)

    gAppConfig, gMqttSetting = loadAppConfig()

    TextInfo = initGUI(MainWin)


    if gAppConfig['AutoStart']:
        print("AutoStart = True")
        #if 'Mqtt' in gAppConfig and len(gAppConfig['Mqtt']) > gMqttSettingIndex:
        #    mqtt_setting = gAppConfig['Mqtt'][gMqttSettingIndex]
        if 'MqttBroker' in gMqttSetting and 'SubTopic' in gMqttSetting:
            broker_port = 1883
            if 'MqttBrokerPort' in gMqttSetting:
                broker_port = gMqttSetting['MqttBrokerPort']
            connectMqttBroker(gMqttSetting['MqttBroker'], broker_port, gMqttSetting['SubTopic'])
    else:
        print("AutoStart = False")


    MainWin.protocol("WM_DELETE_WINDOW", on_closing)
    MainWin.mainloop()

    if gFileWriteThread != None:
        gFileWriteThread.join()

def on_closing():
    global gLabelStatus
    global gAppConfig
    global MainWin

    stopSavingLog()

    #
    # Save last MQTT connection status in APP config.
    #
    str_status = gLabelStatus.cget("text")
    if str_status == STATUS_STR_CONNECTED:
        print("STATUS_STR_CONNECTED")
        gAppConfig['AutoStart'] = True
    elif str_status == STATUS_STR_DISCONNECTED:
        print("STATUS_STR_DISCONNECTED")
        gAppConfig['AutoStart'] = False
    
    saveAppConfig(gAppConfig)

    #
    # Destroy the windows.
    #
    MainWin.destroy()
    #if messagebox.askokcancel("Quit", "Do you want to quit?"):
    #    root.destroy()


def initGUI(win):
    global gFont
    global gAppConfig
    global gMqttSetting
    global gLabelMessage
    global TextInfo
    global gLabelStatus
    global gVarCheckAutoscroll
    global gVarCheckSaveLog
    global gButtonRun

    frame2 = Frame(win)
    frame2["bg"] = WIDGET_BG

    frame3 = Frame(win)
    frame3["bg"] = WIDGET_BG

    frame1 = Frame(win)
    frame1["bg"] = WIDGET_BG

    #frameBottom = Frame(win)
    #frameBottom["bg"] = WIDGET_BG

    str_title = "MqttMonitor %s - https://fw-box.com" % (__version__)
    win.title(str_title)
    win.geometry('670x400')
    win.configure(background=WIN_BG)

    #
    # Frame 2
    #

    textInfoScrollbar = Scrollbar(frame2)
    textInfoScrollbar.pack(side='right', fill='y')

    textInfo = Text(frame2, width=180, height=80, yscrollcommand=textInfoScrollbar.set)
    textInfo.pack()
    textInfo.configure(state='disabled')

    textInfoScrollbar.config(command=textInfo.yview)

    #
    # Frame 1
    #

    col_index = 0

    lbSpace00 = Label(frame1, text=" ")
    lbSpace00["bg"] = WIDGET_BG
    lbSpace00.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    gLabelStatus = Label(frame1, text=STATUS_STR_DISCONNECTED, background='red', font=gFont)
    gLabelStatus.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    lbSpace0 = Label(frame1, text=" ")
    lbSpace0["bg"] = WIDGET_BG
    lbSpace0.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    gButtonMqttSettings = Button(frame1, font=gFont)
    gButtonMqttSettings["bg"] = WIDGET_BG
    gButtonMqttSettings["text"] = "Broker"
    gButtonMqttSettings["command"] = lambda: onClickMqttSettings()
    gButtonMqttSettings.grid(row=0, column=col_index, padx=2, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    textBroker = Text(frame1, width=15, height=1, font=gFont)
    textBroker["bg"] = WIDGET_BG
    textBroker.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1
    textBroker.delete(1.0,"end")
    textBroker.insert(1.0, gMqttSetting['MqttBroker'])

    lbSpace1 = Label(frame1, text=" ")
    lbSpace1["bg"] = WIDGET_BG
    lbSpace1.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    lbPort = Label(frame1, text="Port", font=gFont)
    lbPort["bg"] = WIDGET_BG
    lbPort.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    textPort = Text(frame1, width=6, height=1, font=gFont)
    textPort["bg"] = WIDGET_BG
    textPort.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1
    textPort.delete(1.0,"end")
    textPort.insert(1.0, gMqttSetting['MqttBrokerPort'])

    lbSpace2 = Label(frame1, text=" ")
    lbSpace2["bg"] = WIDGET_BG
    lbSpace2.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    lbSubTopic = Label(frame1, text="Sub Topic", font=gFont)
    lbSubTopic["bg"] = WIDGET_BG
    lbSubTopic.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    textSubTopic = Text(frame1, width=28, height=1, font=gFont)
    textSubTopic["bg"] = WIDGET_BG
    textSubTopic.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1
    textSubTopic.delete(1.0,"end")
    textSubTopic.insert(1.0, gMqttSetting['SubTopic'])

    lbSpace3 = Label(frame1, text=" ")
    lbSpace3["bg"] = WIDGET_BG
    lbSpace3.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    gButtonRun = Button(frame1, font=gFont)
    gButtonRun["bg"] = WIDGET_BG
    gButtonRun["text"] = "Connect"
    gButtonRun["command"] = lambda: onClickConnect(textBroker.get("1.0","end"), textPort.get("1.0","end"), textSubTopic.get("1.0","end"))
    gButtonRun.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    lbSpace5 = Label(frame1, text=" ")
    lbSpace5["bg"] = WIDGET_BG
    lbSpace5.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1


    #
    # Frame 3
    #

    col_index = 0

    gVarCheckAutoscroll = BooleanVar()
    gCheckAutoscroll = Checkbutton(frame3, var=gVarCheckAutoscroll, font=gFont)
    gCheckAutoscroll["bg"] = WIDGET_BG
    gCheckAutoscroll["text"] = "Autoscroll"
    gCheckAutoscroll["command"] = lambda: onClickAutoscroll()
    gCheckAutoscroll.grid(row=0, column=col_index, padx=5, pady=0, ipadx=0, ipady=0)
    if 'Autoscroll' in gAppConfig:
        gVarCheckAutoscroll.set(gAppConfig['Autoscroll'])
    else:
        gVarCheckAutoscroll.set(True)
    col_index = col_index + 1

    lbSpace0 = Label(frame3, text=" ")
    lbSpace0["bg"] = WIDGET_BG
    lbSpace0.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    gButtonClearOutput = Button(frame3, font=gFont)
    gButtonClearOutput["bg"] = WIDGET_BG
    gButtonClearOutput["text"] = "Clear output"
    gButtonClearOutput["command"] = lambda: onClickClearOutput(textInfo)
    gButtonClearOutput.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    lbSpace1 = Label(frame3, text=" ")
    lbSpace1["bg"] = WIDGET_BG
    lbSpace1.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    gVarCheckSaveLog = BooleanVar()
    gCheckSaveLog = Checkbutton(frame3, var=gVarCheckSaveLog, font=gFont)
    gCheckSaveLog["bg"] = WIDGET_BG
    gCheckSaveLog["text"] = "Save log"
    gCheckSaveLog["command"] = lambda: onClickSaveLog()
    gCheckSaveLog.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    if 'SaveLog' in gAppConfig:
        gVarCheckSaveLog.set(gAppConfig['SaveLog'])
    else:
        gVarCheckSaveLog.set(False)
    col_index = col_index + 1

    lbSpace2 = Label(frame3, text=" ")
    lbSpace2["bg"] = WIDGET_BG
    lbSpace2.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    gButtonSettings = Button(frame3, font=gFont)
    gButtonSettings["bg"] = WIDGET_BG
    gButtonSettings["text"] = "Settings"
    gButtonSettings["command"] = lambda: onClickButtonSettings()
    gButtonSettings.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    gLabelMessage = Label(frame3, text="")
    gLabelMessage["bg"] = WIDGET_BG
    gLabelMessage.grid(row=0, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    frame1.pack(padx=2,pady=2,fill='x')
    frame3.pack(padx=2,pady=2,fill='x')
    frame2.pack(padx=2,pady=2)
    #frameBottom.pack(padx=2,pady=2)

    return  textInfo


def addLine(str):
    global gAppConfig
    global gQueueForFile
    global TextInfo
    global gVarCheckAutoscroll
    #print(str)
    if gAppConfig['SaveLog']: # Only put to the queue when the flag is True
        gQueueForFile.put(str)
    TextInfo.configure(state='normal')
    TextInfo.insert(END, str)
    #TextInfo.insert(END, "\n")
    if gVarCheckAutoscroll.get():
        TextInfo.yview(END) # Move the sursor to the end
    TextInfo.configure(state='disabled')


def onClickAutoscroll():
    global gAppConfig
    global gVarCheckAutoscroll
    print("onClickAutoscroll")
    print("gVarCheckAutoscroll=%d" % (gVarCheckAutoscroll.get()))
    gAppConfig['Autoscroll'] = gVarCheckAutoscroll.get()
    saveAppConfig(gAppConfig)

def onClickSaveLog():
    global gAppConfig
    global gVarCheckSaveLog
    global gLabelStatus
    print("onClickSaveLog")
    print("gVarCheckSaveLog=%d" % (gVarCheckSaveLog.get()))
    gAppConfig['SaveLog'] = gVarCheckSaveLog.get()
    saveAppConfig(gAppConfig)
    if gAppConfig['SaveLog']:
        if gLabelStatus['text'] == STATUS_STR_CONNECTED:
            startSavingLog()
    else:
        stopSavingLog()

def onClickClearOutput(textOutput):
    print("onClickClearOutput")
    textOutput.config(state=NORMAL)
    textOutput.delete('1.0', END)
    textOutput.config(state='disabled')

def onClickButtonSettings():
    #global gFont
    global gWinSettings
    global gAppConfig
    global gMqttSetting
    print("onClickButtonSettings")
    #font_sub_win = Font.Font(size = 10, weight = 'bold')
    gWinSettings = Tk()

    win_sub_frame1 = Frame(gWinSettings, bg=WIN_BG)
    win_sub_frame1["bg"] = WIDGET_BG

    gWinSettings.title('Settings')
    gWinSettings.geometry('600x150')
    gWinSettings.configure(background=WIN_BG)


    row_index = 0
    col_index = 0

    lbSpace1 = Label(win_sub_frame1, text="Log path : ", font=gFont)
    lbSpace1["bg"] = WIDGET_BG
    lbSpace1.grid(row=row_index, column=col_index, sticky=E, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    textLogPath = Text(win_sub_frame1, width=45, height=2, font=gFont)
    textLogPath["bg"] = WIDGET_BG
    textLogPath.grid(row=row_index, column=col_index, sticky=W, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    #
    # Clear the textbox and load the setting.
    #
    textLogPath.delete(1.0,"end")
    if 'LogPath' in gAppConfig:
        textLogPath.insert(1.0, gAppConfig['LogPath'])

    gButtonAskDir = Button(win_sub_frame1, font=gFont)
    gButtonAskDir["bg"] = WIDGET_BG
    gButtonAskDir["text"] = "Select"
    gButtonAskDir["command"] = lambda: onClickButtonAskDir(gWinSettings, textLogPath)
    gButtonAskDir.grid(row=row_index, column=col_index, sticky=W, padx=3, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1


    row_index = row_index + 1 # Next line

    spaceRow = Label(win_sub_frame1, text="")
    spaceRow["bg"] = WIDGET_BG
    spaceRow.grid(row=row_index, column=0, columnspan = 3, sticky=W, padx=0, pady=0, ipadx=0, ipady=0)


    row_index = row_index + 1 # Next line

    linkExample = Label(win_sub_frame1, text="Download the Arduino exmaple\nhttps://github.com/fw-box/MqttPrint", fg="blue", cursor="hand2")
    linkExample["bg"] = WIDGET_BG
    linkExample.grid(row=row_index, column=0, columnspan = 3, sticky=W, padx=0, pady=0, ipadx=0, ipady=0)
    linkExample.bind("<Button-1>", lambda e: callbackOpenWeb("https://github.com/fw-box/MqttPrint"))


    #btn_test = Button(win_sub_frame1)
    #btn_test["bg"] = WIDGET_BG
    #btn_test["text"] = "TEST"
    #btn_test["command"] = lambda: onClickTestButton(font_sub_win)
    #btn_test.grid(row=1, column=0, sticky=W, padx=5, pady=0, ipadx=0, ipady=0)

    win_sub_frame1.pack(padx=PAD_X,pady=PAD_Y)

    #font_sub_win.configure(size=16)

def callbackOpenWeb(url):
    webbrowser.open_new(url)

def onClickTestButton(font_sub_win):
    print("onClickTestButton")
    font_sub_win.configure(size=16)

def onClickButtonAskDir(winSettings, textLogPath):
    global gAppConfig

    #
    # Display a dialog
    #
    folder_selected = filedialog.askdirectory()
    print(folder_selected)
    textLogPath.delete(1.0, "end")
    textLogPath.insert(1.0, folder_selected)
    winSettings.focus_force()
    if gAppConfig == None:
        gAppConfig = newAppData()

    #
    # Save to the config file
    #
    gAppConfig['LogPath'] = folder_selected
    saveAppConfig(gAppConfig)

    gLogFileName = renewLogFileName(gAppConfig['LogPath'])
    print("gLogFileName = " + gLogFileName)


def onClickMqttSettings():
    global gFont
    global gAppConfig
    global gMqttSetting
    print("onClickMqttSettings")
    gWinMqttSettings = Tk()

    win_sub_frame1 = Frame(gWinMqttSettings, bg=WIN_BG)
    win_sub_frame1["bg"] = WIDGET_BG

    gWinMqttSettings.title('MQTT Settings')
    gWinMqttSettings.geometry('600x110')
    gWinMqttSettings.configure(background=WIN_BG)

    max_col_count = 0
    row_index = 0
    col_index = 0

    #statusText = StringVar()
    #statusBar = Label(win_sub_frame1, textvariable=statusText, text='status bar', bd=1, relief=SUNKEN, anchor=W)


    lbPort = Label(win_sub_frame1, text="username : ", font=gFont)
    lbPort["bg"] = WIDGET_BG
    lbPort.grid(row=row_index, column=col_index, sticky=E, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    textMqttUsername = Text(win_sub_frame1, width=16, height=1, font=gFont)
    textMqttUsername["bg"] = WIDGET_BG
    textMqttUsername.grid(row=row_index, column=col_index, sticky=W, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1
    textMqttUsername.delete(1.0,"end")
    textMqttUsername.insert(1.0, gMqttSetting['MqttUsername'])

    lbSpace00 = Label(win_sub_frame1, text=" ")
    lbSpace00["bg"] = WIDGET_BG
    lbSpace00.grid(row=row_index, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    lbSubTopic = Label(win_sub_frame1, text="password : ", font=gFont)
    lbSubTopic["bg"] = WIDGET_BG
    lbSubTopic.grid(row=row_index, column=col_index, sticky=E, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    textMqttPassword = Text(win_sub_frame1, width=16, height=1, font=gFont)
    textMqttPassword["bg"] = WIDGET_BG
    textMqttPassword.grid(row=row_index, column=col_index, sticky=W, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1
    textMqttPassword.delete(1.0,"end")
    textMqttPassword.insert(1.0, gMqttSetting['MqttPassword'])

    lbSpace00 = Label(win_sub_frame1, text=" ")
    lbSpace00["bg"] = WIDGET_BG
    lbSpace00.grid(row=row_index, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1

    gButtonSave = Button(win_sub_frame1, font=gFont)
    gButtonSave["bg"] = WIDGET_BG
    gButtonSave["text"] = "Save"
    gButtonSave["command"] = lambda: onClickMqttSettingsSave(textMqttUsername.get("1.0","end"), textMqttPassword.get("1.0","end"), gWinMqttSettings)
    gButtonSave.grid(row=row_index, column=col_index, sticky=W, padx=3, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1
    max_col_count = col_index


    row_index = row_index + 1
    col_index = 0

    lbSpace00 = Label(win_sub_frame1, text=" ")
    lbSpace00["bg"] = WIDGET_BG
    lbSpace00.grid(row=row_index, column=col_index, padx=0, pady=0, ipadx=0, ipady=0)
    col_index = col_index + 1


    #row_index = row_index + 1
    #col_index = 0

    
    #statusBar.grid(row=row_index, column=col_index, columnspan=max_col_count, sticky="nsew", padx=3, pady=0, ipadx=0, ipady=0)
    #col_index = col_index + 1


    win_sub_frame1.pack(padx=PAD_X, pady=PAD_Y)

def onClickMqttSettingsSave(newMqttUsername, newMqttPassword, win):
    global gAppConfig
    global gMqttSetting
    bool_changed, gAppConfig = fixMqttSetting(gAppConfig)
    mqtt_setting_index = gAppConfig['MqttSettingIndex']
    gAppConfig['Mqtt'][mqtt_setting_index]['MqttUsername'] = newMqttUsername.strip()
    gAppConfig['Mqtt'][mqtt_setting_index]['MqttPassword'] = newMqttPassword.strip()
    result = saveAppConfig(gAppConfig)
    if result == True:
        print("Success")
        win.destroy()

    gMqttSetting = gAppConfig['Mqtt'][mqtt_setting_index]

def onClickConnect(broker, port, subTopic):
    global gLabelStatus
    global gAppConfig
    global gClient
    global gSubTopic
    global gMqttRunning
    global gLabelMessage

    new_broker = broker.strip()
    new_port = int(port.strip())
    new_sub_topic = subTopic.strip()
    print(new_broker)
    print(new_port)
    print(new_sub_topic)

    str_status = gLabelStatus.cget("text")
    if str_status == STATUS_STR_CONNECTED:
        print("Try to disconnect")
        #
        # Set the flag to 'False', it would break the MQTT loop and disconnect the MQTT client.
        #
        gMqttRunning = False
    elif str_status == STATUS_STR_DISCONNECTED:
        connectMqttBroker(new_broker, new_port, new_sub_topic)


def connectMqttBroker(newMqttBroker, newMqttBrokerPort, newSubTopic):
    #global gLabelStatus
    global gAppConfig
    global gMqttSetting
    global gClient
    global gSubTopic
    global gMqttRunning
    #global gLabelMessage

    gSubTopic = newSubTopic

    bool_changed, gAppConfig = fixMqttSetting(gAppConfig)
    mqtt_setting_index = gAppConfig['MqttSettingIndex']
    gAppConfig['Mqtt'][mqtt_setting_index]['MqttBroker'] = newMqttBroker.strip()
    gAppConfig['Mqtt'][mqtt_setting_index]['MqttBrokerPort'] = newMqttBrokerPort
    gAppConfig['Mqtt'][mqtt_setting_index]['SubTopic'] = newSubTopic.strip()
    saveAppConfig(gAppConfig)
    gMqttSetting = gAppConfig['Mqtt'][mqtt_setting_index]

    gClient = mqtt.Client()

    if len(gMqttSetting['MqttUsername']) > 0:
        print("MqttUsername:" + gMqttSetting['MqttUsername'])
        print("MqttPassword:" + gMqttSetting['MqttPassword'])
        gClient.username_pw_set(username=gMqttSetting['MqttUsername'], password=gMqttSetting['MqttPassword'])

    gClient.on_connect = on_connect

    gClient.on_disconnect = on_disconnect

    #
    # Set the receiver
    #
    gClient.on_message = on_message

    # 設定登入帳號密碼
    #gClient.username_pw_set("try","xxxx")

    is_ready = True

    try:
        #
        # Set the connection info
        #
        gClient.connect(gMqttSetting['MqttBroker'], gMqttSetting['MqttBrokerPort'], 60)
    except:
        is_ready = False
        showToast("Can't connect to " + gMqttSetting['MqttBroker'])
        print("Can't connect to " + gMqttSetting['MqttBroker'])

    if is_ready == True:
        try:
            gMqttRunning = True
            #
            # Create a thread for MQTT loop
            #
            th = threading.Thread(target = runMqttLoop, args = (gClient, ))
            th.setDaemon(True)#守護執行緒

            #
            # Run it
            #
            th.start()
        except:
            print("Can't start a thread.")


def cleatToast():
    global gLabelMessage
    #print("cleatToast")
    gLabelMessage["text"] = ""

def showToast(message):
    global gLabelMessage
    gLabelMessage["text"] = message
    t = threading.Timer(5, cleatToast)
    t.start()

def loadAppConfig():
    j_data = None

    try:
        with open('MqttMonitor.json', 'r') as read_file:
            j_data = json.load(read_file)
        
        #
        # Check the config data
        #
        if checkSaveAppConfig(j_data): # True : The Settings are changed, reload again.
            print("The Settings are changed, reload again.")
            with open('MqttMonitor.json', 'r') as read_file:
                j_data = json.load(read_file)
    except:
        print("The file 'MqttMonitor.json' doesn't exist.")

    if j_data == None:
        print("Create a new APP data.")
        j_data = newAppData()
        saveAppConfig(j_data)

    current_mqtt_setting_index = j_data['MqttSettingIndex']
    return j_data, j_data['Mqtt'][current_mqtt_setting_index]

def saveAppConfig(jData):
    try:
        ret = json.dumps(jData)
        with open('MqttMonitor.json', 'w') as fp:
            fp.write(ret)
        return True
    except:
        return False

def checkSaveAppConfig(jData):
    update_count = 0
    if 'AutoStart' not in jData:
        jData['AutoStart'] = False
        update_count = update_count + 1
    if 'Autoscroll' not in jData:
        jData['Autoscroll'] = True
        update_count = update_count + 1
    if 'SaveLog' not in jData:
        jData['SaveLog'] = False
        update_count = update_count + 1
    if 'LogPath' not in jData:
        jData['LogPath'] = ""
        update_count = update_count + 1
    bool_changed, jData = fixMqttSetting(jData)
    if bool_changed:
        update_count = update_count + 1

    if update_count > 0:
        saveAppConfig(jData)
        return True
    else:
        return False

def fixMqttSetting(jData):
    global gMqttSetting
    
    update_count = 0
    if 'Mqtt' not in jData or len(jData['Mqtt']) <= 0:
        jData['Mqtt'] = [{"MqttBroker":"broker.emqx.io","MqttBrokerPort":1883,"MqttUsername":"","MqttPassword":"","SubTopic":""}]
        update_count = update_count + 1
    if 'MqttSettingIndex' not in jData:
        jData['MqttSettingIndex'] = 0
        update_count = update_count + 1
    if len(jData['Mqtt']) <= jData['MqttSettingIndex']:
        jData['MqttSettingIndex'] = 0
        update_count = update_count + 1

    gMqttSetting = jData['Mqtt'][jData['MqttSettingIndex']]
    if 'MqttBroker' not in gMqttSetting:
        jData['Mqtt'][jData['MqttSettingIndex']]['MqttBroker'] = "broker.emqx.io"
        update_count = update_count + 1
    if 'MqttBrokerPort' not in gMqttSetting:
        jData['Mqtt'][jData['MqttSettingIndex']]['MqttBrokerPort'] = 1883
        update_count = update_count + 1
    if 'MqttUsername' not in gMqttSetting:
        jData['Mqtt'][jData['MqttSettingIndex']]['MqttBroker'] = ""
        update_count = update_count + 1
    if 'MqttPassword' not in gMqttSetting:
        jData['Mqtt'][jData['MqttSettingIndex']]['MqttPassword'] = ""
        update_count = update_count + 1
    if 'SubTopic' not in gMqttSetting:
        jData['Mqtt'][jData['MqttSettingIndex']]['SubTopic'] = ""
        update_count = update_count + 1

    if update_count > 0:
        gMqttSetting = jData['Mqtt'][jData['MqttSettingIndex']]
        return True, jData
    else:
        return False, jData

def newAppData():
    str_topic = random.choice(string.ascii_lowercase)
    str_topic = str_topic + (''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(15)))
    str_topic = "message/" + str_topic
    print("str_topic=" + str_topic)
    return {"AutoStart":False,"MqttSettingIndex":0,"Mqtt":[{"MqttBroker":"broker.emqx.io","MqttBrokerPort":1883,"MqttUsername":"","MqttPassword":"","SubTopic":str_topic}],"Autoscroll":True,"SaveLog":False,"LogPath":""}

def renewLogFileName(logPath):
    if len(logPath) > 0:
        now = datetime.now() # current date and time
        return logPath + "/" + now.strftime("%Y%m%d%H%M%S.log")
    else:
        return ""

def startSavingLog():
    global gLogFileName
    global gAppConfig
    global gStartSavingLog
    global gFileWriteThread

    if gFileWriteThread != None:
        print("Stop the thread - 'FileWriteThread' firstly.")
        stopSavingLog()

    gLogFileName = renewLogFileName(gAppConfig['LogPath'])
    print("gLogFileName = " + gLogFileName)

    gStartSavingLog = True
    print("Start a new thread - 'FileWriteThread'.")
    gFileWriteThread = FileWriteThread('file_write_queue')
    gFileWriteThread.start()

def stopSavingLog():
    global gLogFileName
    global gStartSavingLog
    global gFileWriteThread

    gLogFileName = ""

    gStartSavingLog = False
    if gFileWriteThread != None:
        gFileWriteThread.join()
        print("Done - gFileWriteThread.join()")
        gFileWriteThread = None

class FileWriteThread(threading.Thread):
    def __init__(self, thread_name):
        super(FileWriteThread, self).__init__(name=thread_name)

    def run(self):
        global gAppConfig
        global gStartSavingLog
        global gQueueForFile

        while gStartSavingLog:
            if gQueueForFile.empty():
                #print('queue is empty')
                pass
            else:
                msg = gQueueForFile.get()
                if len(gLogFileName) > 0:
                    with open(gLogFileName, 'a') as fp:
                        fp.write(msg)
                #print(self.name + ' get ' + msg + ', qsize: ' + str(gQueueForFile.qsize()))
                #print(self.name + ' qsize : ' + str(gQueueForFile.qsize()))
            time.sleep(0.2)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global gAppConfig
    global gLabelStatus
    global gSubTopic
    global gButtonRun
    print("MQTT : Connected with result code " + str(rc))

    if gAppConfig['SaveLog']:
        print("SaveLog is enabled.")
        startSavingLog()
    else:
        print("SaveLog is disabled.")

    if len(gSubTopic) > 0:
        client.subscribe(gSubTopic)
    else:
        showToast("Sub topic is empty.")
        print("Sub Topic is empty.")

    gLabelStatus.configure(background='green')
    gLabelStatus.config(text=STATUS_STR_CONNECTED)
    gButtonRun.config(text="Disconnect")

def on_disconnect(client, userdata, rc):
    global gLabelStatus
    global gMqttRunning
    global gButtonRun
    print("MQTT : Disconnected")
    gLabelStatus.configure(background='red')
    gLabelStatus.config(text=STATUS_STR_DISCONNECTED)
    gButtonRun.config(text="Connect")
    gMqttRunning = False
    stopSavingLog()

#
# The callback for when a PUBLISH message is received from the server.
#
def on_message(client, userdata, msg):
    payload = str(msg.payload, "utf-8")
    #print("MQTT : Message received\n" + payload + "\ntopic : " + msg.topic + "\nretained = " + str(msg.retain))
    addLine(payload)

def runMqttLoop(ObjMqttClient):
    global gMqttRunning
    while gMqttRunning:
        ObjMqttClient.loop() # runs one iteration of the network loop
    print("Disconnect MQTT connection.")
    ObjMqttClient.disconnect() # disconnect gracefully



if __name__ == "__main__":
    main()
