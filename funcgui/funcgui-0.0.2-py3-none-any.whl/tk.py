
import tkinter,os
class python():
    def __init__(self,name):
        self.win = tkinter.Tk()
        self.name = name
        return('换行请用.^表示')

    def b(self):
        while True:
            t1 = tkinter.StringVar()
            tkinter.Entry(self.win, textvariable = t1,width=100).pack()
            tkinter.Button(self.win, text='确定',command=lambda: self.a(t1)).pack() 
            self.win.mainloop()
    def a(self,t1):
        t = t1.get()
        x = '\n'
        for i in range(len(t)):
            if t[i] == '.' and t[i+1] == '^':
                t = t[:i]+x+t[i+1:]
        with open(self.name,'w')as p:
            p.write(t)
            
        os.system('python index.py')