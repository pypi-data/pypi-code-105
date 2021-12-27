import pyloglib

mylog = pyloglib.Log(
    prefix="",
    surfix="",
    splitter=" ",
    time=False , 
    clock=True, 
    saveprefix=True, 
    printprefix=True, 
    savesurfix=True, 
    printsurfix=True, 
    savetime=True, 
    printtime=True, 
    print=True, 
    file=None
)

mylog.log("Hello World!", prefix=None, surfix=None, time=None)
mylog.logtitle("Hello World!")
mylog.lograw("Hello World!")

mylog.remove(1)
mylog.clear()