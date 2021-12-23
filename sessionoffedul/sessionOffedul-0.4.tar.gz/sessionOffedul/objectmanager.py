# Object Manager
# [
# 
# 1 - Questo file contiene tutte le classi (oggetti) che il main.py utilizza.
# 2 - Questo file contiene tutte le funzione per l'object managing.
# 
# TO-DO:
# - 
# -
# -
# -
# -
#
# ]

import json
from typing import List, Tuple

current_json = []
current_item = []
current_objects = []

# / Objects \ 

class Session:
    def __init__(self, session_token, item_list, json_list):
        if session_token == "" or session_token == None: return

        self.secret_token = str(session_token).encode("utf_32")

        try:
            self.item_list = list(item_list)
            self.json_list = list(json_list)
        except:
            return

class IntegerObject:
    def __init__(self, name, value):

        try:
            self.name = name
            self.value = int(value)
            self.type = "Integer"
        except:
            return

    def change(self, field, new_value):
        if field == "name":
            self.name = new_value
        else:
            self.value = int(new_value)

class StringObject:
    def __init__(self, name, value):

        try:
            self.name = name
            self.value = str(value)
            self.type = "String"
        except:
            return

    def change(self, field, new_value):
        if field == "name":
            self.name = new_value
        else:
            self.value = str(new_value)

class TupleObject:
    def __init__(self, name, value):

        try:
            self.name = name
            self.value = tuple(value)
            self.type = "Tuple"
        except:
            return

    def change(self, field, new_value):
        if field == "name":
            self.name = new_value
        else:
            self.value = tuple(new_value)

class ListObject:
    def __init__(self, name, value):

        try:
            self.name = name
            self.value = list(value)
            self.type = "List"
        except:
            return

    def change(self, field, new_value):
        if field == "name":
            self.name = new_value
        else:
            self.value = list(new_value)

class UnknownObject:
    def __init__(self, name, value):

        try:
            self.name = name
            self.value = value
            self.type = "Unknown"
        except:
            return

    def change(self, field, new_value):
        if field == "name":
            self.name = new_value
        else:
            self.value = new_value
# / Functions \ 

def ConvertJsonToObject(_json):
    if _json == None or _json == "": return

    try:
        formattedObject = json.loads(_json)

        if formattedObject['type'] == "Integer":
            obj = IntegerObject(formattedObject['name'], formattedObject['value'])

            return obj
        elif formattedObject['type'] == "String":
            obj = StringObject(formattedObject['name'], formattedObject['value'])

            return obj
        elif formattedObject['type'] == "Tuple":
            obj = TupleObject(formattedObject['name'], formattedObject['value'])

            return obj
        elif formattedObject['type'] == "List":
            obj = ListObject(formattedObject['name'], formattedObject['value'])

            return obj
        else:
            obj = UnknownObject(formattedObject['name'], formattedObject['value'])

            return obj
        
    except:
        return

def AddJson(object):
    # if not isinstance(object, IntegerObject) or not isinstance(object, StringObject) or not isinstance(object, Tuple) or not isinstance(object, ListObject): return

    formattedObject = {
        "name": object.name,
        "value": object.value,
        "type": object.type
    }

    jsonObject = json.dumps(formattedObject)
    current_json.append(jsonObject)
    current_item.append(formattedObject["name"])

def GetObject(name):

    for obj in current_json:

        formattedObject = json.loads(obj)

        if formattedObject['name'] == name:
            return formattedObject['value']
        else:
            del formattedObject
            continue

    return "Object didn't found in current context."

def GetSession():
    for i in current_objects:
        if isinstance(i, Session):
            return i
        else:
            continue

def DeleteObject(name):

    for obj in current_json:

        formattedObject = json.loads(obj)

        if formattedObject['name'] == name:
            current_item.pop(current_item.index(formattedObject['name']))
            current_json.pop(current_json.index(obj))

            return current_json
        else:
            del formattedObject
            continue

def PrintContentOnFile(filename):

    if filename == "" or filename == None: return

    try:
        _file = open(filename + ".json", "a")
        
        for i in current_json:

            unPrettified = json.loads(i)
            prettified = json.dumps(unPrettified, indent=2)

            _file.write("\n" + "\n" + prettified)
    except:
        return

def CreateObject(name, value, _type):

    # AddJson Function

    if _type == int:
        obj = IntegerObject(name, value)

        AddJson(obj)
        return obj
    elif _type == str:
        obj = StringObject(name, value)

        AddJson(obj)
        return obj
    elif _type == tuple:
        obj = TupleObject(name, value)

        AddJson(obj)
        return obj
    elif _type == list:
        obj = ListObject(name, value)

        AddJson(obj)
        return obj
    else:
        obj = UnknownObject(name, value)

        AddJson(obj)
        return obj

def UpdateSession():
    for obj in current_objects:
        if isinstance(obj, Session):
            obj.json_list = current_json
            obj.item_list = current_item
        else:
            continue

def InitializeSession(token):
    
    for obj in current_objects:
        if isinstance(obj, Session):
            return
        else:
            continue
    
    StartSession(token)

def GetJson():

    return current_json


def StartSession(token):
    current_objects.append(Session(token, current_item, current_json))

    
# / Init \

def init():
    pass



if __name__ == "__main__":
    init()
