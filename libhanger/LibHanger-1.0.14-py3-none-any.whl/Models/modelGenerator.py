import os
from numpy import e
import pandas as pd
import csv
import LibHanger.Library.uwGetter as Getter
from pandas.core.frame import DataFrame
from LibHanger.Library.uwExport import ExcelImporter

class modelGenerator(ExcelImporter):
    
    def __init__(self) -> None:
        super().__init__()
        self.fieldTypeMap = {
             'varchar':{'method':'CharFields','columnType':'String'}
            ,'numeric':{'method':'NumericFields','columnType':'Numeric'}
            ,'date':{'method':'DateFields','columnType':'Date'}
            ,'datetime':{'method':'DateTimeFields','columnType':'DateTime'}
            ,'integer':{'method':'IntFields','columnType':'Integer'}
            ,'double':{'method':'FloatFields','columnType':'Float'}
        }
        
    def put_modelByCsv(self):
        
        for sheetname in self.sheets:
            if str(sheetname).startswith(('trn','mst')): 
                # テーブル定義をDataFrameで取得
                df = self.get_TableDefByDataFrame(sheetname)
                # Model内容をpythonファイル出力
                self.put_modelPython(df, sheetname)
                   
    def get_TableDefByDataFrame(self, sheetname):
        
        # シートをdict型に変換
        dict = pd.read_excel(self.filepath, sheet_name=sheetname, skiprows=8, usecols=[1,12,13,14,15,16])
        # dict->DataFrame
        df = pd.DataFrame(dict)
        # DataFrameの列名変更
        df = df.set_axis(['primary_key','fieldname','datatype','default','length','digits'], axis='columns')
        # 欠損値置換
        df = df.fillna({'primary_key': 0, 'fieldname':'','datatype':'','default':'','length':0, 'digits':0})
        # 一部float型をint型に変換
        df['primary_key'] = df['primary_key'].astype(int)
        df['length'] = df['length'].astype(int)
        df['digits'] = df['digits'].astype(int)
        # DataFrameとして返す
        return df
    
    def put_modelPython(self, df:DataFrame, sheetname:str):
        
        # 出力先パス取得
        output_dir = os.path.dirname(self.filepath)
        
        # pythonファイル出力
        with open(os.path.join(output_dir, sheetname + '.py'), 'w', newline='', encoding='utf-8') as f:
            f.writelines('from sqlalchemy.ext.declarative import declarative_base\n')
            f.writelines('import LibHanger.Models.fields as fld\n')
            f.writelines('\n')
            f.writelines('# Baseクラス生成\n')
            f.writelines('Base = declarative_base()\n')
            f.writelines('\n')
            f.writelines('class {0}(Base):'.format(sheetname) + '\n')
            f.writelines('\t\n')
            f.writelines('\t' + '# テーブル名\n')
            f.writelines('\t' + '__tablename__ = \'{0}\''.format(sheetname) + '\n')
            f.writelines('\t\n')
            f.writelines('\t' + '# 列定義\n')
            for index, row in df.iterrows():
                print('LineNo={0}'.format(index))
                outputRow = '\t'  + '{0} = fld.{1}({2})'.format(row['fieldname'],self.get_fieldType_val(row, 'method'), self.get_fieldType_args(row)) + '\n'
                f.writelines(outputRow)
        f.close()
        
    def get_fieldType_val(self, defRow, valType):
        fieldTypeVal:dict = self.fieldTypeMap.get(defRow['datatype'])
        return fieldTypeVal.get(valType)
        
    def get_fieldType_args(self, defRow):
        
        # フィールドタイプ設定
        dataType:str = defRow['datatype']
        if dataType == 'varchar':
            length = [str(defRow['length'])]
            digits = str(defRow['digits']) if defRow['digits'] != 0 else ''
            if digits != '':
                length.append(digits)                
            fieldType = [Getter.getListMargeString(',', length)]
        elif dataType == 'numeric':
            length = [str(defRow['length']), str(defRow['digits']) if defRow['digits'] != '' else '0']
            fieldType = [Getter.getListMargeString(',', length)]
        else:
            fieldType = []

        # 主キー設定
        if defRow['primary_key'] != 0:
            primary_key = 'primary_key=True'
            fieldType.append(primary_key)
        # 既定値設定
        if defRow['default'] != None:
            if dataType == 'varchar':               
                defaultFormat = 'default=\'{0}\''
            else:
                defaultFormat = 'default={0}'
                
            if defRow['default'] == 'NUL':
                default = 'None'
            elif defRow['default'] == '':
                if dataType == 'varchar':
                    default = ''
                else:
                    default = 'None'
            else:
                default = str(int(defRow['default']))
            fieldType.append(defaultFormat.format(default))
        return Getter.getListMargeString(',', fieldType)

            