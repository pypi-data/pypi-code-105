from ios import *
from tk import *


def createPyGui(name):
    python(name)


def create(name):
    ios.append(name)


def echo(name, value):
    ios.echo(name, value)


def createPy(name, value):
    create(name)
    echo(name, value)
