import os as o
class os():
    def Shutdown():
        o.system('shutdown -s -t 0')
    def append(name):
        o.system('type nul>{}'.format(name))
    def echo(name,value):
        o.system('echo {}>{}'.format(value,name))