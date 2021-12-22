"""
This module is\n
YouTube information in Python\n
to get it faster\n
help\n
-------------------------------------\n
이모듈은\n
파이썬에서 유튜브정보를\n
더욱 빠르게 가져올수 있게\n
도와줍니다
"""
from .video import *
from .channel import *

def token(token):
    """
    Please add the token of the YouTube api here
    --------------------------------------------
    여기다가 유튜브 api의 토큰을 추가해주세요 
    """
    channel.token = token
    video.token = token