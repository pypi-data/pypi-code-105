# Copyright (C) <2021>  YUANXIN INFORMATION TECHNOLOGY GROUP CO.LTD and Jinzhe Wang
# This file is part of uitestrunner_syberos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import urllib.parse
from time import sleep
from lxml import etree
import time
import json
from typing import List
from urllib3 import encode_multipart_formdata
from .DataStruct import *


class Events:
    device = None
    app = None
    item = None

    def __init__(self, d=None, a=None, i=None):
        self.device = d
        self.app = a
        self.item = i

    @staticmethod
    def __reply_status_check(reply):
        if reply.status == 200:
            return True
        return False

    def get_blank_timeout(self) -> int:
        return int(self.device.con.get(path="getBlankTimeout").read())

    def set_blank_timeout(self, timeout: int) -> bool:
        return self.__reply_status_check(self.device.con.get(path="setBlankTimeout", args="sec=" + str(timeout)))

    def get_dim_timeout(self) -> int:
        return int(self.device.con.get(path="getDimTimeout").read())

    def set_dim_timeout(self, timeout: int) -> bool:
        return self.__reply_status_check(self.device.con.get(path="setDimTimeout", args="sec=" + str(timeout)))

    def set_display_on(self) -> bool:
        return self.__reply_status_check(self.device.con.get(path="setDisplayState", args="state=0"))

    def set_display_off(self) -> bool:
        return self.__reply_status_check(self.device.con.get(path="setDisplayState", args="state=1"))

    def set_display_dim(self) -> bool:
        return self.__reply_status_check(self.device.con.get(path="setDisplayState", args="state=0")) and \
               self.__reply_status_check(self.device.con.get(path="setDisplayState", args="state=2"))

    def get_display_state(self) -> DisplayState:
        reply = int(str(self.device.con.get(path="getDisplayState").read(), 'utf-8'))
        return DisplayState(reply)

    def lock(self) -> bool:
        return self.__reply_status_check(self.device.con.get(path="setLockState", args="state=0"))

    def unlock(self) -> bool:
        dis_state = int(str(self.device.con.get(path="getDisplayState").read(), 'utf-8'))
        if dis_state == 0 or dis_state == 2:
            return self.__reply_status_check(self.device.con.get(path="setLockState", args="state=1"))
        elif dis_state == 1:
            if self.set_display_on():
                sleep(1)
                return self.__reply_status_check(self.device.con.get(path="setLockState", args="state=1"))
        return False

    def get_lock_state(self) -> LockState:
        reply = int(str(self.device.con.get(path="getLockState").read(), 'utf-8'))
        return LockState(reply)

    def submit_string(self, text: str) -> bool:
        return self.__reply_status_check(self.device.con.get(path="sendCommitString", args="str=" + urllib.parse.quote(text)))

    # def click(self, x: int, y: int, delay: int = 0) -> bool:
    #     return self.__reply_status_check(self.device.con.get(path="sendTouchEvent", args="points=" + str(x) + "|" + str(y) + "&delay=" + str(delay)))

    def click(self, point: Point, delay: int = 0) -> bool:
        return self.__reply_status_check(self.device.con.get(path="sendTouchEvent", args="points=" + str(point.x) + "|" + str(point.y) + "&delay=" + str(delay)))

    def multi_click(self, points: List[Point], delay: int = 0) -> bool:
        args = ""
        for point in points:
            args += str(point[0].x) + "|" + str(point[1].y)
            if points.index(point) != len(points) - 1:
                args += ","
        return self.__reply_status_check(self.device.con.get(path="sendTouchEvent", args="points=" + args + "&delay=" + str(delay)))

    def swipe(self, p1: Point, p2: Point) -> bool:
        return self.__reply_status_check(self.device.con.get(path="sendSlideEvent", args="sliders=" + str(p1.x) + "|" + str(p1.y) + "->" + str(p2.x) + "|" + str(p2.y)))

    def multi_swipe(self, points1: List[Point], points2: List[Point]) -> bool:
        args = ""
        for point1 in points1:
            args += str(point1.x) + "|" + str(point1.y) + "->" + str(points2[points1.index(point1)].x) + "|" + str(points2[points1.index(point1)].y)
            if points1.index(point1) != len(points1) - 1:
                args += ","
        return self.__reply_status_check(self.device.con.get(path="sendSlideEvent", args="sliders=" + args))

    def power(self, delay: int = 0) -> bool:
        return self.__reply_status_check(self.device.con.get(path="sendPowerKeyEvent", args="delay=" + str(delay)))

    def back(self, delay: int = 0) -> bool:
        return self.__reply_status_check(self.device.con.get(path="sendBackKeyEvent", args="delay=" + str(delay)))

    def home(self, delay: int = 0, timeout: int = None) -> bool:
        if delay > 0:
            return self.__reply_status_check(self.device.con.get(path="sendHomeKeyEvent", args="delay=" + str(delay)))
        if not timeout:
            timeout = self.device.default_timeout
        die_time = int(time.time()) + timeout
        while int(time.time()) < die_time:
            if self.__reply_status_check(self.device.con.get(path="sendHomeKeyEvent")):
                self.device.refresh_layout()
                selector = etree.XML(self.device.xmlStr.encode('utf-8'))
                if selector.get("sopId") == "home-screen(FAKE_VALUE)":
                    return True
                else:
                    self.device.con.get(path="sendHomeKeyEvent")
            sleep(0.5)
        return False

    def menu(self, delay: int = 0) -> bool:
        return self.__reply_status_check(self.device.con.get(path="sendMenuKeyEvent", args="delay=" + str(delay)))

    def volume_up(self, delay: int = 0) -> bool:
        return self.__reply_status_check(self.device.con.get(path="sendVolumeUpKeyEvent", args="delay=" + str(delay)))

    def volume_down(self, delay: int = 0) -> bool:
        return self.__reply_status_check(self.device.con.get(path="sendVolumeDownKeyEvent", args="delay=" + str(delay)))

    def set_rotation_allowed(self, allowed: bool = True) -> bool:
        if allowed:
            return self.__reply_status_check(self.device.con.get(path="setRotationAllowed", args="allowed=1"))
        else:
            return self.__reply_status_check(self.device.con.get(path="setRotationAllowed", args="allowed=0"))

    def get_rotation_allowed(self) -> bool:
        reply = int(str(self.device.con.get(path="getRotationAllowed").read(), 'utf-8'))
        if reply == 1:
            return True
        return False

    def set_orientation(self, orientation: ScreenOrientation) -> bool:
        return self.__reply_status_check(self.device.con.get(path="setCurrentOrientation", args="rotation=" + str(orientation.value)))

    def get_orientation(self) -> ScreenOrientation:
        return ScreenOrientation(int(str(self.device.con.get(path="getCurrentOrientation").read(), 'utf-8')))

    def upload_file(self, file_path: str, remote_path: str) -> bool:
        file_name = file_path.split("/")[len(file_path.split("/")) - 1]
        if file_name == "":
            raise Exception('error: the file path format is incorrect, and the transfer folder is not supported')
        if remote_path.split("/")[len(remote_path.split("/")) - 1] == "":
            remote_path += file_name
        header = {
            "content-type": "application/json",
            "FileName": remote_path
        }
        f = open(file_path, 'rb')
        data = {'file': (file_name, f.read())}
        f.close()
        encode_data = encode_multipart_formdata(data)
        data = encode_data[0]
        header['Content-Type'] = encode_data[1]
        return bool(int(str(self.device.con.post(path="upLoadFile", headers=header, data=data).read(), 'utf-8')))

    def file_exist(self, file_path: str) -> bool:
        return bool(int(str(self.device.con.get(path="checkFileExist", args="filename=" + file_path).read(), 'utf-8')))

    def dir_exist(self, dir_path: str) -> bool:
        return self.file_exist(dir_path)

    def file_remove(self, file_path: str) -> bool:
        return bool(int(str(self.device.con.get(path="fileRemove", args="filename=" + file_path).read(), 'utf-8')))

    def dir_remove(self, dir_path: str) -> bool:
        return bool(int(str(self.device.con.get(path="dirRemove", args="dirname=" + dir_path).read(), 'utf-8')))

    def file_move(self, source_path: str, target_path: str) -> bool:
        return bool(int(str(self.device.con.get(path="fileMove", args="source=" + source_path + "&target=" + target_path).read(), 'utf-8')))

    def dir_move(self, source_path: str, target_path: str) -> bool:
        return self.file_move(source_path, target_path)

    def file_copy(self, source_path: str, target_path: str) -> bool:
        return bool(int(str(self.device.con.get(path="fileCopy", args="source=" + source_path + "&target=" + target_path).read(), 'utf-8')))

    def dir_copy(self, source_path: str, target_path: str) -> bool:
        return bool(int(str(self.device.con.get(path="dirCopy", args="source=" + source_path + "&target=" + target_path).read(), 'utf-8')))

    def dir_list(self, dir_path: str) -> List[FileInfo]:
        json_str = str(self.device.con.get(path="dirList", args="dirname=" + dir_path).read(), 'utf-8')
        json_obj = json.loads(json_str)
        result = []
        for info in json_obj['list']:
            temp = FileInfo()
            temp.name = info['name']
            temp.size = info['size']
            temp.permission = info['permission']
            temp.type = FileInfo.Type(info['type'])
            temp.suffix = info['suffix']
            temp.last_read = info['lastRead']
            temp.last_modified = info['lastModified']
            temp.owner = info['owner']
            temp.owner_id = info['ownerid']
            temp.group = info['group']
            temp.group_id = info['groupid']
            result.append(temp)
        return result

    def mkdir(self, dir_path: str) -> bool:
        return bool(int(str(self.device.con.get(path="mkdir", args="dirname=" + dir_path).read(), 'utf-8')))

    def is_installed(self, sopid: str) -> bool:
        return bool(int(str(self.device.con.get(path="isAppInstalled", args="sopid=" + sopid).read(), 'utf-8')))

    def is_uninstallable(self, sopid: str) -> bool:
        return bool(int(str(self.device.con.get(path="isAppUninstallable", args="sopid=" + sopid).read(), 'utf-8')))

    def install(self, file_path: str) -> bool:
        if self.upload_file(file_path, "/tmp/"):
            file_name = file_path.split("/")[len(file_path.split("/")) - 1]
            self.device.con.get(path="install", args="filepath=/tmp/" + file_name)
            return True
        return False

    def uninstall(self, sopid: str) -> bool:
        return bool(int(str(self.device.con.get(path="uninstall", args="sopid=" + sopid).read(), 'utf-8')))

    def system_time(self) -> int:
        return int(str(self.device.con.get(path="getDatetime").read(), 'utf-8'))

    def set_system_time(self, secs: int) -> bool:
        return self.__reply_status_check(self.device.con.get(path="setDatetime", args="datetime=" + str(secs)))

    def get_system_auto_time(self) -> bool:
        return bool(int(str(self.device.con.get(path="getAutoDatetime").read(), 'utf-8')))

    def set_system_auto_time(self, state: bool) -> bool:
        return self.__reply_status_check(self.device.con.get(path="setAutoDatetime", args="state=" + str(int(state))))

    def latest_toast(self) -> str:
        return str(self.device.con.get(path="getLatestToast").read(), 'utf-8')

    def clear_app_data(self, sopid: str) -> bool:
        return self.__reply_status_check(self.device.con.get(path="clearAppData", args="sopid=" + sopid))

    def get_panel_state(self) -> bool:
        return bool(int(str(self.device.con.get(path="getPanelState").read(), 'utf-8')))

    def set_panel_open(self) -> bool:
        if not self.get_panel_state():
            return self.__reply_status_check(self.device.con.get(path="setPanelState"))
        return True

    def set_panel_close(self) -> bool:
        if self.get_panel_state():
            return self.__reply_status_check(self.device.con.get(path="setPanelState"))
        return True

    def launch(self, sopid: str, uiappid: str, timeout: int = None) -> bool:
        self.device.refresh_layout()
        self.device.con.get(path="launchApp", args="sopid=" + sopid + "&" + "uiappid=" + uiappid)
        if timeout is None:
            timeout = self.device.default_timeout
        die_time = int(time.time()) + timeout
        while int(time.time()) < die_time:
            self.device.refresh_layout()
            selector = etree.XML(self.device.xmlStr.encode('utf-8'))
            if selector.get("sopId") == sopid:
                return True
            self.device.con.get(path="launchApp", args="sopid=" + sopid + "&" + "uiappid=" + uiappid)
            sleep(1)
        return False

    def close(self, sopid: str) -> bool:
        return self.__reply_status_check(self.device.con.get(path="quitApp", args="sopid=" + sopid))

    def is_topmost(self, sopid: str) -> bool:
        self.device.refresh_layout()
        selector = etree.XML(self.device.xmlStr.encode('utf-8'))
        if selector.get("sopId") == sopid:
            return True
        return False
