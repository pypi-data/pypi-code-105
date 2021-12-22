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

import enum


class FileInfo:
    """
    文件/文件夹信息\n
    name: 名称\n
    type: 类型\n
    size: 大小(byte)\n
    suffix: 后缀(最后一个"."符号之后的字符串，如果没有则为空字符串)\n
    permission: 权限的数字表示\n
    last_modified: 最后修改时间(秒)\n
    last_read: 最后读取时间(秒)\n
    owner: 拥有者名称\n
    owner_id: 拥有者ID\n
    group: 用户组名称\n
    group_id: 用户组ID
    """
    class Type(enum.Enum):
        """
        文件类型\n
        FILE: 文件(包括有效的符号连接)\n
        DIRECTORY: 文件夹\n
        OTHER: 其他类型
        """
        OTHER = -1
        FILE = 0
        DIRECTORY = 1
    name = str()
    type = Type
    size = int()
    suffix = str()
    permission = int()
    last_modified = int()
    last_read = int()
    owner = str()
    owner_id = int()
    group = str()
    group_id = int()


class Point:
    """
    坐标点\n
    x: 横向坐标点\n
    y: 纵向坐标点
    """
    x = int()
    y = int()

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class LockState(enum.Enum):
    """
    锁屏状态\n
    LOCKED: 已锁定\n
    UNLOCKED: 已解锁
    """
    LOCKED = 0
    UNLOCKED = 1


class DisplayState(enum.Enum):
    """
    显示器状态\n
    ON: 亮屏\n
    OFF: 灭屏\n
    DIM: 暗屏
    """
    ON = 0
    OFF = 1
    DIM = 2


class ScreenOrientation(enum.Enum):
    """
    屏幕方向\n
    PRIMARY: 主要方向 一般为0度\n
    PORTRAIT: 纵向 一般为0度\n
    LANDSCAPE: 横向 一般为90度\n
    INVERTED_PORTRAIT: 反纵向 一般为180度\n
    INVERTED_LANDSCAPE: 反横向 一般为270度
    """
    PRIMARY = 0
    PORTRAIT = 1
    LANDSCAPE = 2
    INVERTED_PORTRAIT = 3
    INVERTED_LANDSCAPE = 4


class Controller(enum.Enum):
    """
    控制端类型\n
    ANYWHERE: 非兼容平台\n
    WINDOWS_AMD64: x86_64架构的windows平台，推荐windows10\n
    LINUX_X86_64: x86_64架构的linux平台，推荐ubuntu18.04\n
    DARWIN_X86_64: x86_64架构的macOSX平台，推荐Catalina
    """
    ANYWHERE = 0
    WINDOWS_AMD64 = 1
    LINUX_X86_64 = 2
    DARWIN_X86_64 = 3
