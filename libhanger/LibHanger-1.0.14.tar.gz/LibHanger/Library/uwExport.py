import pandas as pd

class BaseExport():
    pass

class BaseImport():
    pass

class ExcelImporter(BaseImport):
    
    def __init__(self):
        self.workbooks = None
        self.sheets = None
        self.filepath = None
        
    def openBook(self, filePath):
        
        # ファイルパス保持
        self.filepath = filePath
        # ブックの読み込み
        self.workbooks = pd.ExcelFile(filePath)
        # シートの読み込み
        self.sheets = self.workbooks.sheet_names
        
class ExcelExporter(BaseExport):
    pass
