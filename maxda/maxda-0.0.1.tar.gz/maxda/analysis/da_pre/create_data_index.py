# -*- coding: utf-8 -*-
# ----------------------------------------------
# purpose : 创建数据id
# author : 
# create_time : 2020/7/3 13:28
# update_time : 2020/7/3 13:28
# copyright : Lavector
# ----------------------------------------------
import uuid

from maxda.analysis.analysis_interface import *


class CreateDataIndex(RowInterface):
    def __init__(self):
        super(CreateDataIndex, self).__init__(None)

    def process(self, data=None, **params):
        return str(uuid.uuid1()).replace("-", "")
