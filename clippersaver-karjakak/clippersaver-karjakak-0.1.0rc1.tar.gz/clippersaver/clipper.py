from tkinter import Tk, ttk, simpledialog, messagebox
import tkinter as tk
from Clien.clien import cmsk
import sys, os
import subprocess
import ctypes
import ctypes.wintypes as w

# Ref from: https://stackoverflow.com/questions/
# 46132401/read-text-from-clipboard-in-windows-using-ctypes
# 53226110/how-to-clear-clipboard-in-using-python/53226144


class Clipper:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipper")
        self.root.resizable(False, False)

        self.aft = None
        self.upt = tuple()
        self.sel = []
        self.coll = set()

        self.ls = tk.Listbox(root, selectmode="multiple")
        self.ls.pack(pady=2, padx=2)
        self.ls.bind("<ButtonRelease>", self.updatesel)

        self.bto = ttk.Button(root, text="Start clipping!", command=self.clipon)
        self.bto.pack(pady=1, padx=2)

        self.bts = ttk.Button(root, text="Stop clipping!", command=self.stc)
        self.bts.pack(pady=1, padx=2)

        self.btp = ttk.Button(root, text="Structure", command=self.struc)
        self.btp.pack(pady=1, padx=2)

        self.clipon()

    def updatesel(self, event=None):
        if self.upt:
            if set(self.ls.curselection()) - set(self.upt):
                x = list(set(self.ls.curselection()) - set(self.upt)).pop()
                self.sel.append(x)
                self.upt = self.ls.curselection()
            elif set(self.upt) - set(self.ls.curselection()):
                x = list(set(self.upt) - set(self.ls.curselection())).pop()
                del self.sel[self.sel.index(x)]
                self.upt = self.ls.curselection()
        else:
            self.upt = self.ls.curselection()
            self.sel.append(self.upt[0])

    def copasw(self) -> str:

        CF_UNICODETEXT = 13

        u32 = ctypes.WinDLL("user32")
        k32 = ctypes.WinDLL("kernel32")

        OpenClipboard = u32.OpenClipboard
        OpenClipboard.argtypes = (w.HWND,)
        OpenClipboard.restype = w.BOOL
        GetClipboardData = u32.GetClipboardData
        GetClipboardData.argtypes = (w.UINT,)
        GetClipboardData.restype = w.HANDLE
        GlobalLock = k32.GlobalLock
        GlobalLock.argtypes = (w.HGLOBAL,)
        GlobalLock.restype = w.LPVOID
        GlobalUnlock = k32.GlobalUnlock
        GlobalUnlock.argtypes = (w.HGLOBAL,)
        GlobalUnlock.restype = w.BOOL
        EmptyClipboard = u32.EmptyClipboard
        CloseClipboard = u32.CloseClipboard
        CloseClipboard.argtypes = None
        CloseClipboard.restype = w.BOOL

        text = ""
        if OpenClipboard(None):
            h_clip_mem = GetClipboardData(CF_UNICODETEXT)
            text = ctypes.wstring_at(GlobalLock(h_clip_mem))
            GlobalUnlock(h_clip_mem)
            EmptyClipboard()
            CloseClipboard()
        del (
            OpenClipboard,
            GetClipboardData,
            GlobalLock,
            GlobalUnlock,
            EmptyClipboard,
            CloseClipboard,
            u32,
            k32,
            CF_UNICODETEXT,
        )
        return text

    def pbcopas(self) -> str:

        if sys.platform.startswith("win"):
            if gt := self.copasw():
                return gt
        else:
            with subprocess.Popen(
                "pbpaste",
                stdout=subprocess.PIPE,
                bufsize=1,
                universal_newlines=True,
                text=True,
            ) as p:
                if gt := p.stdout.read():
                    os.system("pbcopy < /dev/null")
            return gt

    def clipon(self):
        if self.root.focus_get() == None:
            self.root.focus_force()
        clip = self.pbcopas()

        match clip:
            case "":
                self.aft = self.root.after(500, self.clipon)
            case _:
                self.ls.insert(self.ls.winfo_cells() + 1, clip)
                self.aft = self.root.after(500, self.clipon)

    def stc(self):
        if self.aft:
            self.root.after_cancel(self.aft)
            self.aft = None

    def struc(self):
        coll = []
        if self.sel:

            class MyDialog(simpledialog.Dialog):
                def body(self, master):
                    tk.Label(master, text="Pass: ").grid(row=0, column=0, sticky=tk.E)
                    self.e1 = tk.Entry(master, show="-")
                    self.e1.grid(row=0, column=1)
                    tk.Label(master, text="Var: ").grid(row=1, column=0, sticky=tk.E)
                    self.e2 = tk.Entry(master)
                    self.e2.grid(row=1, column=1)
                    return self.e1

                def apply(self):
                    if self.e1.get() and self.e2.get():
                        self.result = (
                            self.e1.get(),
                            self.e2.get(),
                        )
                    else:
                        self.result = None

            d = MyDialog(self.root)
            if d.result:
                for i in self.sel:
                    coll.append(self.ls.get(i))
                cmsk("".join(coll), d.result[0], d.result[1])
            self.ls.selection_clear(0, tk.END)
            self.sel = []
            self.upt = tuple()
        del coll


def main():
    root = Tk()
    start = Clipper(root)
    start.root.mainloop()


if __name__ == "__main__":
    main()
