# -*- coding: utf-8 -*-

import platform
import sys
import os


class loadBaseUtil(object):
    instance = None
    # 是否初始化过
    init_flag = False

    code_root = ''
    baseStr = ''

    objUtils = None
    fileUtils = None
    simhash = None
    params = vars()

    def __new__(cls, *args, **kwargs):
        # 1.判断类属性是否为空对象，若为空说明第一个对象还没被创建
        if cls.instance is None:
            # 2.对第一个对象没有被创建，我们应该调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
        # 3.把类属性中保存的对象引用返回给python的解释器
        return cls.instance

    def __init__(self, code_root):
        if loadBaseUtil.init_flag:
            return

        print("初始化 loadBaseUtil")

        self.code_root = code_root

        if platform.system().lower() == 'windows':
            self.baseStr = os.path.join(code_root, 'common-baseutil')
        elif platform.system().lower() == 'linux':
            self.baseStr = '/root/dataAlg/common-baseutil'
        sys.path.append(self.baseStr)
        print(self.baseStr)

        import baseUtils

        self.objUtils = baseUtils.objUtils(code_root)
        self.fileUtils = baseUtils.fileUtils()
        self.simhash = baseUtils.SimHash()

        self.params = vars(self.objUtils.set_params())

        loadBaseUtil.init_flag = True

        print("初始化 loadBaseUtil 结束")
