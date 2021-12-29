# This Python file uses the following encoding: utf-8
import logging
import random

from airtest.core import api
from airtest.core.android.adb import *
#import logging


class byteClickLiveRoomFunction:

    def __init__(self):
    #    logging.basicConfig(filename='logging.txt', level='info')
        self.BYTEDANCE_TITOK_APP_NAME = "com.ss.android.ugc.aweme"

    def __connect_biubiu_device(self, biubiu_device=None):
        # 如果biubiu_device不为空，检查设备连接状态
        if biubiu_device is not None:
            if self.check_device_connect(biubiu_device):
                api.init_device('Android', biubiu_device)  # 初始化设备
                self.device = api.device()
            else:
                pass
        else:
            api.init_device('Android')
            self.device = api.device()

    def __restartDouyinApp(self):
        """
        重启抖音app
        """
        api.stop_app(self.BYTEDANCE_TITOK_APP_NAME)
        api.sleep(0.2)
        api.start_app(self.BYTEDANCE_TITOK_APP_NAME)
        api.sleep(3)
        return self.device.get_default_device()

    def __inLiveRoom(self, roomName):
        """
        搜索进入直播间
        :param roomName: 直播间名称
        """
        api.touch((650, 105))
        api.sleep(1)
        api.text(roomName)
        api.sleep(2)
        api.touch((650, 105))  # 点击搜索
        api.sleep(2)
        api.touch((random.uniform(95.0, 500.0), random.uniform(650.0, 1300.0)))

    def __login(self, numb):
        """
        账号登录

        登录场景: 1、输入验证码登录，2、发送短信验证码登录

        :param numb: 登录账号
        :param loginType: 登录场景
        :return: void
        """
        """调出登录框"""
        api.touch((666, 1548))
        api.sleep(1)
        # 判断当前手机是否登录
        if api.exists(api.Template(r"../static/tpl1639111764435.png", record_pos=(-0.001, -0.482),
                                   resolution=(720, 1600))):  # 如果存在登录框
            # 为保险 先点一下输入框
            api.touch((388, 425))
            api.sleep(1)
            logging.info("手机号", numb)
            print(numb)
            api.text(numb)
            api.sleep(1)
            api.touch((415, 575))
            api.sleep(1)
            api.touch((361, 714))

        return self.device.get_default_device()

    def __send_live_text(self, biubiu_context):
        """
        发送文字弹幕
        :param biubiu_context: 文本内容
        :return: void
        """
        # 随机点击屏幕 初始化窗口
        api.touch((random.uniform(151.0, 1500.0), 700))
        api.sleep(random.uniform(0.3, 1.0))

        api.touch((96, 1563))  # 输入框初始位置
        api.sleep(random.uniform(0.3, 1.0))  # 随机时间
        api.touch((573, 1506))  # 弹出输入小键盘图标位置
        api.sleep(random.uniform(0.3, 1.0))
        api.text(biubiu_context, False)
        api.sleep(random.uniform(0.3, 1.0))
        api.touch((666, 966))  # //文本发送位置

    def __while_send_text(self, biubiu_context, biubiu_count):
        """
        循环发送弹幕内容
        :param biubiu_context: 弹幕内容
        :param biubiu_count: 发送次数
        :return: void
        """
        i = 0
        while i < biubiu_count:
            self.__send_live_text(biubiu_context)

            i += 1

    def __send_sms(self, smsBody='YZ', smsNum='106916613659103'):
        """
        发送短信
        :param smsBody: 短信内容
        :param smsNum: 目标号码
        :return: void
        """
        shellStr = 'am start -a android.intent.action.SENDTO -d sms:%s --es sms_body %s' % (smsNum, smsBody)
        api.shell(shellStr)
        api.sleep(1)
        api.touch((660, 1536))
        # 验证码发送后执行
        api.sleep(2)
        self.__sms_after_verify()

    def __sms_after_verify(self):
        """
        短信发送成功后执行操作
        """
        api.start_app(self.BYTEDANCE_TITOK_APP_NAME)
        api.touch((random.uniform(141.0, 500.0), 693))
        api.sleep(random.uniform(0.3, 0.8))
        api.touch((random.uniform(250.0, 489.0), 789))

    def __send_live_emoji(self, emoji=(354, 1140)):
        """
        发送表情弹幕
        :param emoji: 表情坐标
        :return: void
        """
        # 随机点击屏幕 初始化窗口
        api.touch((random.uniform(141.0, 1500.0), 700))
        api.sleep(random.uniform(0.3, 1.0))

        # emoji 坐标
        api.touch((96, 1563))  # 输入框初始位置
        api.sleep(random.uniform(0.3, 1.0))  # 随机时间
        api.touch((573, 1506))  # 弹出输入小键盘图标位置
        api.sleep(random.uniform(0.3, 1.0))
        api.touch(emoji)
        api.sleep(random.uniform(0.3, 1.0))
        api.touch((666, 966))

    def check_device_connect(self, deviceSerialno):
        """
        检查设备链接状态
        """
        adb = ADB()
        return adb.devices().count((deviceSerialno, 'device')) > 0

    def get_quick_biubiu_text(self, FilePath='Messages.txt'):
        """
        获取快捷语
        """
        fileInfo = open(FilePath, mode='r', encoding="UTF-8-sig")
        fileInfoLines = fileInfo.readlines()
        fileInfo.close()
        return fileInfoLines

    def get_device_info_list(self, device_list_file="device_list.txt"):
        """
        获取设备列表
        已连接设备列表应该加入缓存文件，
        列表重缓存读取
        刷新列表==刷新缓存列表
        """
        fileInfo = open(device_list_file, mode='r', encoding="UTF-8-sig")
        fileInfoLines = fileInfo.readlines()

        fileInfo.close()

        deviceList = []
        for devInfoStr in fileInfoLines:
            devInfoList = devInfoStr.replace('\n', '').split(' ')

            if len(devInfoList) == 2:
                devInfoList.append("未设置")

            if self.check_device_connect(devInfoList[0]):

                devInfo = {
                    "device": devInfoList[0],
                    "devNumber": devInfoList[1],
                    "userName": devInfoList[2]
                }

                deviceList.append(devInfo)
            else:
                logging.debug("连接失败: %s - %s " % (devInfoList[1], devInfoList[0]))

        return deviceList

    def init_biubiu_server(self, biubiu_context="", biubiu_count=1, biubiu_type="text", biubiu_device=None, login_verify_type=1,
                           login_verify_number=106916613659103):
        """
        初始化入口
        :param biubiu_context: 内容 必须 : 弹幕内容、表情包内容、直播间房号、登录名、验证码内容
        :param biubiu_count: 执行次数
        :param biubiu_type: 操作类型 text:文字内容 emoji:表情 favour:疯狂点赞 in_live_room:进入直播间 login:登录 login_verify:验证码 restart_douyin_app:重启抖音App
        :param biubiu_device: 设备号：安卓序列号
        :param login_verify_type: 登录验证码场景，1.接受验证码验证 2.发送短信验证码验证 3.确认验证码的操作
        :param login_verify_number: 手机号
        :return: void

        """
        self.__connect_biubiu_device(biubiu_device)

        # api.init_device('Android', biubiu_device)  # 初始化设备

        # 登录账号
        if biubiu_type == "login":
            # 启动抖音APP
            self.__restartDouyinApp()
            api.sleep(6)
            self.__login(biubiu_context)

        # 进入直播间
        if biubiu_type == "in_live_room":
            self.__inLiveRoom(biubiu_context)

        # 发弹幕
        if biubiu_type == "text":
            # 调用循环发送弹幕
            self.__while_send_text(biubiu_context, biubiu_count)

        if biubiu_type == "emoji":
            # 发送表情
            self.__send_live_emoji(biubiu_context)

        if biubiu_type == "login_verify":
            if login_verify_type==1:
                pass
            elif login_verify_type==2:
                self.__send_sms(biubiu_context, login_verify_number)

        if biubiu_type == "restart_douyin_app":
            self.__restartDouyinApp()
