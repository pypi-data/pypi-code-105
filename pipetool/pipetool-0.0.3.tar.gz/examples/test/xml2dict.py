# coding= utf-8
'''
Created on 2021-8-30

@author: 86139
'''
import xmltodict
import json

def xml2dict():
    file_object = open('test.xml',encoding = 'utf-8')                                                                                                            
    try:
        all_the_xmlStr = file_object.read()
    finally:
        file_object.close()
    #xml To dict 
    convertedDict = xmltodict.parse(all_the_xmlStr)
    print(convertedDict['annotation'])
    #ensure_ascii 设置为False 中文可以转换
    jsonStr = json.dumps(convertedDict,ensure_ascii=False)
    print( jsonStr);
    #写入文件 写入为utf-8编码
    with open('./result.json', 'w',encoding = 'utf-8') as f:
    #除去xmltodict 转换时默认添加的'@' 符号
        f.write(jsonStr.replace('@', ''))


    #2.Json to Xml
    dictVal = {
        'page': {
        'title': 'xxx',
        'ns': 0,
        'revision': {
            'id': 123456,
            }
        }
    }
    convertedXml = xmltodict.unparse(dictVal);
    print ("convertedXml=",convertedXml)
if __name__ == '__main__':
    xml2dict();