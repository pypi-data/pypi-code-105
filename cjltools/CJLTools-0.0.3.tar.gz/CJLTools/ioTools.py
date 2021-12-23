# -*- coding: utf-8 -*-
# @File    :   ioTools.py
# @Time    :   2021/12/23 17:10:06
# @Author  :   Cen Jinglun
# @Contact :   cenjinglun@qq.com

import yaml
import json
from PIL import Image


def read_yml(path):
    try:
        with open(path, 'r') as f:
            content = yaml.safe_load(f)
        return content
    except IOError:
        print(f'YML File Error at {path}')


def read_json(path):
    try:
        with open(path, 'r') as f:
            dicts = json.load(f)
        return dicts
    except IOError:
        print(f'Json File Error at {path}')


def read_image(path):
    try:
        img = Image.open(path).convert("RGB")
        return img
    except IOError:
        print(f'Image File Error at {path}')
