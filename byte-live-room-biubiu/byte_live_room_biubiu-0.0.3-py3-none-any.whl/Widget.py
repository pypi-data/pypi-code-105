# This Python file uses the following encoding: utf-8
# UI pyside6-uic form.ui > formUi.py
# build  cmd pyinstaller --name="zhibozhushou" --windowed --onefile Widget.py
from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QErrorMessage, QMessageBox

from byte_live_room_biubiu.byteClickLiveRoomFunction import *
from byte_live_room_biubiu.formUi import Ui_Widget


# 创建一个Widget类并继承QWidget
class Widget(QWidget):

    def __init__(self):
        super().__init__()
        # logging.basicConfig(filename="logging.txt", level=logging.INFO)
        self.QErrorMessage = QErrorMessage()
        self.messageBox = QMessageBox()
        self.byteClickFunction = byteClickLiveRoomFunction()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        # 初始化登录框设备
        self.ui.deviceSerialNumberInput.setItemText(0, None)
        # 加载快捷语
        self.ui.quickTextsAllRoomSelectOption.setItemText(0, None)
        self.setRightTipContentWidgetTipTextLayoutText('正在加载快捷语....')
        for BiubiuMessage in self.byteClickFunction.get_quick_biubiu_text('./Messages.txt'):
            BiubiuMessage = BiubiuMessage.replace("\n", "")
            if (BiubiuMessage is not None) and (BiubiuMessage != ""):
                self.ui.quickTextsAllRoomSelectOption.addItem(BiubiuMessage)
        self.setRightTipContentWidgetTipTextLayoutText('快捷语加载完毕！')
        self.setRightTipContentWidgetTipTextLayoutText('正在加载设备列表...')
        try:
            self.showDeviceListBox()

            self.ui.restartAppButton.clicked.connect(self.restartDouyinApp)  # 重启app
            self.ui.inLiveRoomButton.clicked.connect(self.in_live_room)  # 进直播间
            self.ui.reloadDeviceListButton.clicked.connect(self.reloadshowDeviceListBox)  # 重载设备列表
            self.ui.sendQuickTextAllRoomInputButton.clicked.connect(self.sendQuickTextAllRoomInputfunction)  # 发送输入框文字

        except ValueError as E:
            self.setRightTipContentWidgetTipTextLayoutText('正在加载失败！')
            self.QErrorMessage.showMessage(E)
        self.setRightTipContentWidgetTipTextLayoutText('设备加载完成！')
        self.ui.login.accepted.connect(self.device_user_login)

    def device_user_login(self):
        """
        登录抖音账号
        """
        device_name = self.ui.deviceSerialNumberInput.currentData()
        login_user = self.ui.userInputLogin.text().replace('\n', '').replace(' ', '')
        print(login_user)
        print(device_name, login_user)
        if (device_name is None) or (device_name == ""):
            return self.setRightTipContentWidgetTipTextLayoutText('<font color=red>错误：请选择要登录的设备</font>')
        elif (login_user is None) or (login_user == ""):
            return self.setRightTipContentWidgetTipTextLayoutText('<font color=red>错误：登录账号不能为空！</font>')
        else:
            # 根据设备名获取设备编号
            self.byteClickFunction.init_biubiu_server(biubiu_type='login', biubiu_device=device_name,
                                                      biubiu_context=login_user)

    def get_device_info_list(self):
        return self.byteClickFunction.get_device_info_list()

    def sendQuickTextAllRoomInputfunction(self, biubiu_device=False):
        """
        发送批量输入框文字
        """
        sendText = self.ui.sendAllLiveRoomTextInput.text()
        self.send_biubiu_text(sendText, biubiu_device)

    @QtCore.Slot()
    def restartDouyinApp(self, biubiu_device=False):
        """
        重启抖音app, 如果设备编码为空， 重启全部设备
        """
        if not biubiu_device:
            for deviceInfo in self.get_device_info_list():
                # 检查设备连接状态
                if self.byteClickFunction.check_device_connect(deviceInfo['device']):
                    self.currectDeviceInfo = deviceInfo
                    self.restartDouyinApp(deviceInfo['device'])
                else:
                    self.setRightTipContentWidgetTipTextLayoutText(
                        "<font color=red> %s 掉线了，重启失败 </font>" % (deviceInfo['devNumber'],))
        else:
            self.byteClickFunction.init_biubiu_server(biubiu_context=None,
                                                      biubiu_device=biubiu_device,
                                                      biubiu_type='restart_douyin_app')

            self.setRightTipContentWidgetTipTextLayoutText(
                "%s 启动 %s 成功" % (self.currectDeviceInfo['devNumber'], '抖音App'))

    def in_live_room(self, liveRoomName=False, biubiu_device=False):
        """
        进入直播间，如果设备编码为空，所有设备进入
        """
        if not liveRoomName:
            liveRoomName = self.ui.inLiveRoomNameInput.text()
        if not biubiu_device:
            for deviceInfo in self.get_device_info_list():
                if self.byteClickFunction.check_device_connect(deviceInfo['device']):
                    self.currectDeviceInfo = deviceInfo
                    self.in_live_room(liveRoomName=liveRoomName, biubiu_device=deviceInfo['device'])
                else:
                    self.setRightTipContentWidgetTipTextLayoutText(
                        "<font color=red> %s 掉线了，进入失败 </font>" % (deviceInfo['devNumber'],))

        else:
            self.byteClickFunction.init_biubiu_server(biubiu_context=liveRoomName, biubiu_device=biubiu_device,
                                                      biubiu_type='in_live_room')

    def send_biubiu_text(self, biubiu_text, biubiu_device=False):
        """
        发送弹幕
        如果biubiu_device为空，则群发
        """
        if not biubiu_device:
            for deviceInfo in self.get_device_info_list():
                # 检查设备连接状态
                if self.byteClickFunction.check_device_connect(deviceInfo['device']):
                    self.send_biubiu_text(biubiu_text, biubiu_device=deviceInfo['device'])
                else:
                    self.setRightTipContentWidgetTipTextLayoutText("%s 掉线了, 弹幕发送失败" % (deviceInfo['devNumber'],))
        else:
            self.byteClickFunction.init_biubiu_server(biubiu_context=biubiu_text, biubiu_count=1,
                                                      biubiu_device=biubiu_device)
            self.setRightTipContentWidgetTipTextLayoutText("%s" % (biubiu_text,))

    def showDeviceListBox(self):
        """
        显示已连接设备列表
        """
        for deviceInfo in self.get_device_info_list():
            print(deviceInfo)
            _deviceNumber = deviceInfo['devNumber']

            self.deviceWidget = QtWidgets.QLabel(_deviceNumber + " - " + deviceInfo['userName'],  # 创建一个文本对象
                                                 alignment=QtCore.Qt.AlignLeft)
            self.deviceWidget.setObjectName(_deviceNumber)

            self.ui.devicesGroupBox.addWidget(self.deviceWidget)
            self.ui.deviceSerialNumberInput.addItem(deviceInfo['devNumber'], deviceInfo['device'])

            self.setRightTipContentWidgetTipTextLayoutText("%s 连接成功" % _deviceNumber)

    def reloadshowDeviceListBox(self):
        """
        重载设备列表
        """
        widgetCount = self.ui.devicesGroupBox.count()
        if widgetCount >= 1:
            for i in range(widgetCount):
                self.ui.devicesGroupBox.itemAt(i).widget().deleteLater()
        else:
            False

        return self.showDeviceListBox()

    def setRightTipContentWidgetTipTextLayoutText(self, message: str):
        """
        写入信息框内容
        """
        self.ui.RightTipContentWidgetTipTextLayout.addWidget(
            QtWidgets.QLabel(message, alignment=QtCore.Qt.AlignLeft))


