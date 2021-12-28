
def hkmUpdateYaml(newValue):
    key_ = []
    if isinstance(newValue,dict):
        for key,value in newValue.items():
            f = hkmUpdateYaml(value)
            if isinstance(f,list):
                [key_.append(key.replace('.','_@_')+"."+x) for x in f]
            else:
                if not f:
                    key_.append(key.replace('.','_@_')+"=~'~'~")
                else:
                    key_.append(key.replace('.','_@_')+"="+str(f))
        return key_
    else:
        if isinstance(newValue,str):
            return newValue.replace('.','_@_')
        if isinstance(newValue,bool):
            if newValue:
                return "true"
            else:
                return "false"
        if isinstance(newValue,list):
            return ','.join(newValue)

def reCheckValue(value,mdic = None):
    if not mdic:
        myDic = {} 
        if not value:
            return ""
        else:
            r = value[0]
            value.pop(0)
            if r.find('=') > 0:
                ar = r.split('=')
                myDic[ar[0]] = ar[1]
                return myDic
            else:
                myDic[r] = reCheckValue(value)
                return myDic
    else:
        r = value[0]
        value.pop(0)
        if r.find('=') > 0:
            ar = r.split('=')
            mdic[ar[0]] = ar[1].replace("~'~'~","")
            return mdic
        else:
            mdic[r] = reCheckValue(value)
            return mdic
    
    
def dict_merge(dct, merge_dct):
    dic = {}
    if merge_dct:
        for k, v in merge_dct.items():
            if (k in dct and isinstance(dct[k], dict)):
                if isinstance(v,dict):
                    dic = dict_merge(dct[k],v)
                else:
                    dic[k] = v
            else:
                dct[k] = v
                
    return dic


            

def hkmRewriteUpdate(value):
    myDic = {}
    
    if isinstance(value,list):
        
        for i in value:
            v = i.split('.')
            d = reCheckValue(v,{})
            myDic = myDic | dict_merge(myDic,d)
    else:
        if isinstance(value,str):
            v = value.split('.')
            d = reCheckValue(v,{})
            myDic = myDic | dict_merge(myDic,d)
    
    return myDic

if __name__ == "__main__" :
    pass
    # print(hkmRewriteUpdate('shamav=hakimu'))
            