"""
  UIE Rewrite.
  UIE - Universal Integer Encoding. Is instrument for encrypting\decrypting data.

  Written by ftdot, unkawn, theskrutter (Group AncapWL)
"""

import binascii
from . import UCErrors
from .modes import *

class UIECoder:

  def __init__(self, key:str, key_mode:UIEKeyMode=KeyMode.uD, result_mode:UIEResultMode=ResultMode.uB64, splitter='\\', dict_='qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMЙЦУКЕЁНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮйцукеёнгшщзхъфывапролджэячсмитьбю1234567890~`!@#$%^&*()-+_=\\/|\\{\\} \':"<>?,.'):
    """
      Creates UIECoder object, for encrypt\decrypt by UIE algorithm.
      key - A key for encrypt\decrypt.
      result_mode - A returning
    """
    self.key = key
    self.key_mode = key_mode
    self.result_mode = result_mode

    self.splitter = splitter
    self.dict = dict_

  def _encrypt(self, text, key, splitter, dict_):
    def en(s,key):
      num=0
      d=dict_
      for a in d:
        num+=1
        if a==s:r=num
      return int(int(r*key*key)*2)+1
    i = len(text) - 1
    text_ = ''
    while i >= 0:
      text_ = text_ + text[i]
      i = i - 1
    encoded=''
    for s in text_: encoded+=splitter+str(en(s,key))
    encoded_ = []
    for i, c in enumerate(encoded):
      key_c = ord(str(key)[i % len(str(key))])
      t_c = ord(c)
      encoded_.append(chr((t_c + key_c) % 127))
    return ''.join(encoded_)

  def _decrypt(self, text, key, splitter, dict_):
    decoded = []
    for i,c in enumerate(text):
      key_c=ord(str(key)[i % len(str(key))])
      enc_c=ord(c)
      decoded.append(chr((enc_c - key_c) % 127))
    decoded_= ''.join(decoded)
    decoded=''
    d=dict_
    for s in decoded_.split(splitter):
      if s!='':
        try:onum=int((int(s)/key/key)/2-1)
        except:pass
        try:decoded+=d[int(onum)]
        except:pass
      i=len(decoded)-1
    decoded_=''
    while i >= 0:
      decoded_=decoded_+decoded[i]
      i=i - 1
    return decoded_

  def key_to_int(self, key):
    """
      Translate key to integer.
    """
    key=binascii.hexlify(key.encode('utf-8')).decode()
    lst='0123456789'
    for c in key:
      if c not in lst:
        key=key.replace(c,'')
    return int(key)

  def encrypt(self, text):
    """
      Encrypting text to UIE.
      text - Text to encrypt.
    """
    # Generating key (need int)
    key, error = self.key_mode(self.key).getkey()
    if error: # Raise an error, if key mode gave error.
      raise UCErrors.KeyModeError(f"KeyMode gave error: {error}")

    # Encrypting
    result = self._encrypt(text, self.key_to_int(key), self.splitter, self.dict)

    result, error = self.result_mode(result).getencrypted()
    if error: # Raise an error, if text mode gave error.
      raise UCErrors.TextModeError(f"TextMode gave error: {error}")

    return result

  def decrypt(self, encrypted):
    """
      Decrypts UIE encrypted text.
      encrypted - Encrypted UIE text.
    """
    # Generating key (need int)
    key, error = self.key_mode(self.key).getkey()
    if error: # Raise an error, if key mode gave error.
      raise UCErrors.KeyModeError(f"KeyMode gave error: {error}")

    # Getting text by TextMode processing
    encrypted, error = self.result_mode(encrypted).getdecrypted()
    if error: # Raise an error, if text mode gave error.
      raise UCErrors.TextModeError(f"TextMode gave error: {error}")

    # Decrypting
    result = self._decrypt(encrypted, self.key_to_int(key), self.splitter, self.dict)

    return result