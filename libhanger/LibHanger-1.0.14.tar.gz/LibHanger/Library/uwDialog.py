import tkinter as tk
from tkinter import filedialog

class baseDialog:
    
    def unVisibleRootWindow(self):
        root = tk.Tk()
        root.withdraw()

class uwFileDialog(baseDialog):
    
    class fileTypes:
        
        excelBook_xlsxOnly = [('Excel ブック','*.xlsx')]
        excelBook = [('Excel ブック','*.xlsx,*.xls')]
        csv = [('CSV (コンマ区切り)','*.csv')]
        pdf = [('PDF','*.pdf')]
        any = {('*', '*.*')}
        
    def __init__(self) -> None:
        super().__init__()
        
    def openFileDialog(self, fileType:fileTypes):
            
        # ルートウィンドウ非表示
        self.unVisibleRootWindow()
        
        # ファイル参照ダイアログを開く
        return filedialog.askopenfilename(filetypes=fileType)

class uwFolderDialot(baseDialog):

    def openFolderDialog(self):
        
        # ルートウィンドウ非表示
        self.unVisibleRootWindow()

        # フォルダ参照ダイアログを開く
        return filedialog.askdirectory()