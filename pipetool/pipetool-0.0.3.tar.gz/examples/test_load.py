'''
Created on 2021-8-30

@author: 86139
'''
import pipetool as ptl


def test_xml_load():
    data = ptl.load('test/test.xml')
    print(data['annotation'])
    

def test_json_dump():
    obj = {'and':1}
    data = ptl.dump(obj,file='dump.json',file_format='json')
#     print(data)
    

def test_xml_dump():
    obj = {'and':1}
    data = ptl.dump(obj,file_format='xml')
    print(data)
    
    
def test_xml_dump_file():
    obj = {'and':1}
    ptl.dump(obj,'dump.xml',file_format='xml') 

 
def test_csv_load():
    data = ptl.load('test/test.csv')
    print(type(data))
    
    
def test_csv_dump():
    obj = {'and':1}
    data = ptl.dump(obj,file_format='csv')
    print(data)
    
    
def test_csv_dump_file():
    obj = []
    obj2 = {'and':1}
    obj3 = {'accnd':'中午'}
    obj.append(obj2) 
    obj.append(obj3) 
    ptl.dump(obj,'dump.csv') 
    data = ptl.dump(obj,file_format='csv') 
    print(data)
  
if __name__=='__main__':
    test_csv_dump_file()