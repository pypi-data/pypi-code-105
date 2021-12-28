import os
import re

def get_dict_key(dic, value):
        keys = list(dic.keys())
        values = list(dic.values())
        idx = values.index(value)
        key = keys[idx]
        return key

class ENC:
    def __init__(self, message):
        self.cd={
            "a":"0a",
            "b":"0b",
            "c":"0c",
            "d":"0d",
            "e":"0e",
            "f":"0f",
            "g":"0g",
            "h":"0h",
            "i":"0i",
            "j":"0j",
            "k":"0k",
            "l":"0l",
            "m":"0m",
            "n":"0n",
            "o":"0o",
            "p":"0p",
            "q":"0q",
            "r":"0r",
            "s":"0s",
            "t":"0t",
            "u":"0u",
            "v":"0v",
            "w":"0w",
            "x":"0x",
            "y":"0y",
            "z":"0z",
            "none":"/none",
            "A":"/-\\",
            "B":"|))",
            "C":"(c",
            "D":"|)",
            "E":"|~-_",
            "F":"|~-",
            "G":"(-|",
            "H":"|-|",
            "I":"~|_",
            "J":"-|_!",
            "K":"|/\\",
            "L":"|_",
            "M":"|^\/^|",
            "N":"|\|",
            "O":"0xO()",
            "P":"||)",
            "Q":"()_",
            "R":"|)\\",
            "S":"(\)",
            "T":"-+|",
            "U":"~+|_|+~",
            "V":"+\/+",
            "W":"\/\/",
            "X":"\+/",
            "Y":"`|`",
            "Z":"~/_+",
            "`":"*`",
            "~":"*~",
            "!":"*!",
            "@":"*@",
            "#":"*#",
            "$":"*$",
            "%":"*%",
            "^":"*^",
            "&":"*&",
            "*":"**",
            "(":"*(",
            ")":"*)",
            "_":"*_",
            "-":"*-",
            "+":"*+",
            "=":"*=",
            "{":"*{",
            "}":"*}",
            "[":"*[",
            "]":"*]",
            ":":"*:",
            ";":"*;",
            "0":"0x0000",
            "1":"0x0001",
            "2":"0x0002",
            "3":"0x0003",
            "4":"0x0004",
            "5":"0x0005",
            "6":"0x0006",
            "7":"0x0007",
            "8":"0x0008",
            "9":"0x0009",
            "PYmili":"(世界上最帅的男人)",
            }
        self.x=[]
        self.y=[]
        for x,y in self.cd.items():
            self.x.append(x)
            self.y.append(y)
        self.msg=message
    def enc(self):
        self._msg_=[]
        zhun=[]
        num=0
        for msg in self.msg:
            zhun.append(msg)
            if zhun[num] in self.cd.keys():
                self._msg_.append(self.cd[zhun[num]])
            else:
                self._msg_.append(zhun[num])
            num+=1
        return ";".join(self._msg_)
    def dec(self,message=None):
        _zhuan_=[]
        if message == None:
            for msg in ";".join(self._msg_).split(';'):
                if msg in self.cd.values():
                    _zhuan_.append(str(get_dict_key(self.cd, msg)))
                else:
                    _zhuan_.append(msg)
        else:
            for msg in message.split(';'):
                if msg in self.cd.values():
                    _zhuan_.append(str(get_dict_key(self.cd, msg)))
                else:
                    _zhuan_.append(msg)
        return "".join(_zhuan_)
