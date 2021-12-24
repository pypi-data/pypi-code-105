# Copyright (c) OpenMMLab. All rights reserved. 

import xmltodict
from .base import BaseFileHandler
 

class XmlHandler(BaseFileHandler): 
 
    
    def load_from_fileobj(self, file):  
        try:
            all_the_xmlStr = file.read()
        finally:
            file.close()
        return xmltodict.parse(xml_input = all_the_xmlStr)

    def dump_to_fileobj(self, obj, file, **kwargs): 
        xmltodict.unparse(obj,output=file, **kwargs)  

    def dump_to_str(self, obj, **kwargs):  
        return xmltodict.unparse(obj, **kwargs) 
    