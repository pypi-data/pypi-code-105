# ----- pyloglib -----
# Python Logging Library
# v1.0.6

from datetime import datetime

class Log:
    def __init__(
        self, 
        prefix="", 
        surfix="",
        splitter=" ",
        time=False,
        clock=True,
        saveprefix=True, 
        printprefix=True, 
        savesurfix=True, 
        printsurfix=True, 
        savetime=True, 
        printtime=True, 
        print=True, 
        file=None,
        ):

        self.prefix = prefix
        self.surfix = surfix
        self.splitter = splitter
        self.time = time
        self.clock = clock
        self.saveprefix = saveprefix
        self.printprefix = printprefix
        self.savesurfix = savesurfix
        self.printsurfix = printsurfix
        self.savetime = savetime
        self.printtime = printtime
        self.print = print
        self.file = file
        
        self.loglist = []

        try:
            with open(self.file, 'r') as file:
                self.loglist = []
                for i in file.readlines():
                    self.loglist.append(i.replace('\n', ''))
        except: pass

    def log(self, content, prefix=None, surfix=None, time=None):
        currenttime = str(datetime.date(datetime.now())).split("-")
        currenttime.reverse()
        if self.clock == True:
            currenttime = datetime.now().strftime("%H:%M:%S") + "-" + "-".join(currenttime) + self.splitter
        else:
            currenttime = "-".join(currenttime) + self.splitter

        if self.print == True:
            printedlog = ""
            if prefix != None and self.printprefix == True:
                printedlog = f"{prefix}"
            elif self.printprefix == True:
                printedlog = f"{self.prefix}"
            if self.time == True and self.printtime == True and time != False:
                printedlog = printedlog + f"{currenttime}"
            elif time == True: printedlog = printedlog + f"{currenttime}"
            printedlog = printedlog + f"{content}"
            if surfix != None and self.printsurfix == True:
                printedlog = printedlog + f"{surfix}"
            elif self.printsurfix == True:
                printedlog = printedlog + f"{self.surfix}"
            print(printedlog)
        
        if self.file != None:
            with open(self.file, 'a') as file:
                savedlog = ""
                if prefix != None and self.saveprefix == True:
                    savedlog = f"{prefix}"
                elif self.saveprefix == True:
                    savedlog = f"{self.prefix}"
                if self.time == True and self.savetime == True and time != False:
                    savedlog = savedlog + f"{currenttime}"
                elif time == True: savedlog = savedlog + f"{currenttime}"
                savedlog = savedlog + f"{content}"
                if surfix != None and self.savesurfix == True:
                    savedlog = savedlog + f"{surfix}"
                elif self.printsurfix == True:
                    savedlog = savedlog + f"{self.surfix}"
                file.write(f"{savedlog}\n")
        
            self.loglist.append(savedlog)
        return f"{self.prefix}{currenttime}{content}{self.surfix}"

    def logtitle(self, content):

        if self.print == True:
            print(f"============ {content} ============")
        if self.file != None:
            with open(self.file, 'a') as file:
                file.write(f"============ {content} ============\n")

        self.loglist.append(f"============ {content} ============")
        return f"============ {content} ============"

    def lograw(self, content):

        if self.print == True:
            print(content)
        if self.file != None:
            with open(self.file, 'a') as file:
                file.write(f"{content}\n")

        self.loglist.append(content)
        return content
    
    def clear(self):
        self.loglist = []
        if self.file != None:
            with open(self.file, 'w'): pass
    
    def remove(self, number):
        self.loglist = self.loglist[:len(self.loglist) - number]
        if self.file != None:
            with open(self.file, 'w') as file:
                if len(self.loglist) != 0:
                    file.write("\n".join(self.loglist) + "\n")
                else: 
                    with open(self.file, 'w'): pass