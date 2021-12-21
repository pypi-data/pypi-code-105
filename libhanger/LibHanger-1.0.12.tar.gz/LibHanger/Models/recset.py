import inspect
import pandas as pd
import copy

class recset():
    
    def __init__(self, t) -> None:
        self.modelType = t
        self.rows = []
        self.__columns = self.__getColumnAttr()
        self.__primaryKeys = self.__getPrimaryKeys()
    
    def __getColumnAttr(self):
        attributes = inspect.getmembers(self.modelType, lambda x: not(inspect.isroutine(x)))
        return list(filter(lambda x: not(x[0].startswith("__") or x[0].startswith("_") or x[0] == "metadata" or x[0] == "registry"), attributes))
    
    def __getPrimaryKeys(self):
        primaryKeys = []
        for col in self.__columns:

            # 主キーリスト作成            
            memberInvoke = getattr(self.modelType, col[0])            
            if memberInvoke.primary_key == True:
                primaryKeys.append(col[0])
                
        return primaryKeys
    
    def newRow(self):
        return self.rowSetting(self.modelType())
        
    def rowSetting(self, row):
        
        for col in self.__columns:

            # Modelのインスタンス変数取得
            memberInvoke = getattr(self.modelType, col[0])
            # 既定値の設定
            setattr(row, col[0], memberInvoke.default.arg)
                                     
        return row
    
    def columns(self):
        return self.__columns
    
    def addRow(self, row):
        self.rows.append(row)
    
    def eof(self):
        return False if len(self.rows) > 0 else True
    
    def primaryKeys(self):
        return self.__primaryKeys
    
    def getDataFrame(self):
        
        # 行インスタンスをDeepCopy
        targetRows = copy.deepcopy(self.rows)
        # DataFrame化で不要な列を削除
        for rowInstance in targetRows:
            delattr(rowInstance, '_sa_instance_state')
        # 行インスタンスをリスト化
        rowlist = list(map(lambda f: vars(f), targetRows))

        # rowlistをDataFrame変換
        df = pd.DataFrame(rowlist)
        
        # DataFrameに主キー設定
        if len(self.__primaryKeys) > 0:
            df = df.set_index(self.__primaryKeys, drop=False)
            
        # 戻り値を返す
        return df