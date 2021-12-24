# Copyright (c) OpenMMLab. All rights reserved. 
 
from .base import BaseFileHandler  
import pandas as pd 

class CsvHandler(BaseFileHandler): 
 
    
    def load_from_fileobj(self, file, **kwargs):    
        return pd.read_csv(file, **kwargs)

    def dump_to_fileobj(self, obj, file, **kwargs): 
        df = pd.DataFrame(obj)   
        kwargs.setdefault('sep', '\t')  
        kwargs.setdefault('header', None)  
        kwargs.setdefault('index', None) 
        kwargs.setdefault('encoding', 'utf-8') 
        df.to_csv(file, **kwargs)

    def dump_to_str(self, obj, **kwargs):  
        df = pd.DataFrame(obj)     
        return df.to_string(**kwargs)
    
    
    