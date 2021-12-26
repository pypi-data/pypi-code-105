# coding:utf-8
import tkinter
import os
from tkinter import ttk


class python():
    def __init__(self, name, windowName='createPy'):
        self.win = tkinter.Tk()
        self.win.title(windowName)
        self.l = tkinter.Label(self.win, text='')
        self.l.pack()
        if '.py' in name:
            self.name = name
        else:
            self.name = name+'.py'
        while True:
            a = tkinter.Label(
                self.win, text='换行请用. ^ 表示。For line breaks, please use ".^" express.')
            a.pack()
            t1 = tkinter.StringVar()
            tkinter.Entry(self.win, textvariable=t1, width=100).pack()
            c = ttk.Button(self.win, text='确定',
                           command=lambda: self.a(t1)) or tkinter.Button(self.win, text='确定', command=lambda: self.a(t1))
            c.pack()
            self.win.mainloop()

    def a(self, t1):
        t = t1.get()
        x = '\n'
        for i in range(len(t)):
            if t[i] == '.' and t[i+1] == '^':
                t = t[:i]+x+t[i+2:]
        with open(self.name, 'w')as p:
            p.write(t)
        self.l.config(text='生成成功, 正在运行中。Build succeeded and is running.')
        os.system('python ./{}'.format(self.name))
        self.l.config(text='运行成功。run successfully.')
        self.l.pack()
