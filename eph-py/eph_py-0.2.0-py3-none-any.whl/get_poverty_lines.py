import pandas as pd
import wget
import pyreadr
import os

def get_poverty_lines(regional=False):
    if not regional:
        if os.path.exists("canastas.rds"):
            os.remove("canastas.rds")
        wget.download("https://github.com/holatam/data/raw/master/eph/canasta/canastas.rds","canastas.rds")
        df = pyreadr.read_r('canastas.rds')[None] 
    else:
        df = pd.read_excel('https://www.indec.gob.ar/ftp/cuadros/sociedad/serie_cba_cbt.xls',skiprows = range(1, 8), names=['periodo', 'CBA', 'ICE', 'CBT'])
        df.dropna(inplace=True)
    return df