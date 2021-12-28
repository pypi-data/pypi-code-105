import pyloglib

mylog = pyloglib.Log(
    prefix="",
    suffix="",
    splitter=" ",
    time=False , 
    clock=True, 
    saveprefix=True, 
    printprefix=True, 
    savesuffix=True, 
    printsuffix=True, 
    savetime=True, 
    printtime=True, 
    print=True, 
    file=None
)

mylog.log("Hello World!", prefix=None, suffix=None, time=None)
mylog.logtitle("Hello World!")
mylog.lograw("Hello World!")

mylog.remove(1)
mylog.clear()