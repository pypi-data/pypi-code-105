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
    文件/文件夹信息
    name: 名称
    type: 类型
    size: 大小(byte)
    suffix: 后缀(最后一个"."符号之后的字符串，如果没有则为空字符串)
    permission: 权限的数字表示
    last_modified: 最后修改时间(秒)
    last_read: 最后读取时间(秒)
    owner: 拥有者名称
    owner_id: 拥有者ID
    group: 用户组名称
    group_id: 用户组ID
    """
    class Type(enum.Enum):
        """
        文件类型
        FILE: 文件(包括有效的符号连接)
        DIRECTORY: 文件夹
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
    坐标点
    x: 横向坐标点
    y: 纵向坐标点
    """
    x = int()
    y = int()

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class LockState(enum.Enum):
    """
    锁屏状态
    LOCKED: 已锁定
    UNLOCKED: 已解锁
    """
    LOCKED = 0
    UNLOCKED = 1


class DisplayState(enum.Enum):
    """
    显示器状态
    ON: 亮屏
    OFF: 灭屏
    DIM: 暗屏
    """
    ON = 0
    OFF = 1
    DIM = 2


class ScreenOrientation(enum.Enum):
    """
    屏幕方向
    PRIMARY: 主要方向 一般为0度
    PORTRAIT: 纵向 一般为0度
    LANDSCAPE: 横向 一般为90度
    INVERTED_PORTRAIT: 反纵向 一般为180度
    INVERTED_LANDSCAPE: 反横向 一般为270度
    """
    PRIMARY = 0
    PORTRAIT = 1
    LANDSCAPE = 2
    INVERTED_PORTRAIT = 3
    INVERTED_LANDSCAPE = 4
