from osys import *
from tk import *

def createPyGui(name):
    python(name)
def shutdown():
    os.Shutdown()
def create(name):
    os.append(name)
def echo(name,value):
    os.echo(name,value)
def createPy(name,value):
    create(name)
    echo(name,value)