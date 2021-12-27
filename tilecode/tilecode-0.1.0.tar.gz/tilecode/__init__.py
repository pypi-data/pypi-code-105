__version__ = '0.1.0'

def tilePrint(val):
  print(val)
def tileInput(val):
  input(val)
def tileAbs(val):
  abs(val)
def tileMod(num1, num2):
  print(num1 % num2)
def tileCreateVar(name, val):
  print("This does not work currently. Sorry for any inconvience.")
def tileRun():
  print("This does not work currently. Sorry for any inconvience.")
def tileGet(name):
  print("This does not work currently. Sorry for any inconvience.")
def tileRound(val, place):
  print(round(val, place))
def tileDisplayImg(src):
  print("This does not work currently. Sorry for any inconvience.")
def tileCreate(name, val):
  file = open(name, "x")
  file.write(val)
def tileDelete(name):
  import os
  os.delete(name)
def tileAdd(name, val):
  file = open(name, "a")
  file.write(val)
def tileOpen(name):
  file = open(name, "r")
  print(file.read(name))
def tileJoin(val1, val2):
  print(val1 + val2)