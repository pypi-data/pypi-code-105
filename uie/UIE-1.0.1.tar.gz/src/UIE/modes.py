"""
  UIE Modes.
  Coded by unkawn.
"""

import hashlib
from base64 import b64encode, b64decode

class UIEKeyMode:

  def __init__(self, key):
    self.key = key

  def getkey(self): # RESULT, ERROR
    return None, "Method not overwritten"

class UIEResultMode:

  def __init__(self, text):
    self.text = text

  def getencrypted(self): # RESULT, ERROR
    return None, "Method not overwritten"

  def getdecrypted(self): # RESULT, ERROR
    return None, "Method not overwritten"

class KeyMode:

  class uD(UIEKeyMode):
    def getkey(self):
      return self.key, None

  class u1(UIEKeyMode):
    def getkey(self):
      result = hashlib.sha1(self.key).hexdigest()
      return result, None

  class u256(UIEKeyMode):
    def getkey(self):
      result = hashlib.sha256(self.key).hexdigest()
      return result, None

  class uM5(UIEKeyMode):
    def getkey(self):
      result = hashlib.md5(self.key).hexdigest()
      return result, None

class ResultMode:

  class uR(UIEResultMode):
    def getencrypted(self):
      return self.text, None
    def getdecrypted(self):
      return self.text, None

  class uB64(UIEResultMode):
    def getencrypted(self):
      try:
        bytesresult = b64encode(self.text.encode('UTF-8'))
        result = bytesresult.decode()
        return result, None
      except Exception as e:
        return None, str(e)
    def getdecrypted(self):
      try:
        bytesresult = b64decode(self.text.encode('UTF-8'))
        result = bytesresult.decode()
        return result, None
      except Exception as e:
        return None, str(e)