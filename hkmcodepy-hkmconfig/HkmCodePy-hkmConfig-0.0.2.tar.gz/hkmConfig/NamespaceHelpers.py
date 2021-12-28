from Hkm_Bin.App import App
from yamlConfig.YamlParse import YamlParse
from Helpers.ConfigHelper import hkmRewriteUpdate, hkmUpdateYaml

def hkmEnvFormat(source:str):
    yaml = YamlParse()
    data = hkmUpdateYaml(yaml.GET(source))
    return data

def __cfg__(cof):
    
    cof.INITIALISING_DEFAULT()
    config = cof.config_file
    prties = []
    data = hkmEnvFormat('configuration.yaml')
    
    if isinstance(data,list):
        for x in data:
            ar = x.split('.') 
            cf = ar[0]
            ar.pop(0)
            if cf == config:
                prties.append(hkmRewriteUpdate(".".join(ar)))
    
    for yz in prties:
        for pr,valu in yz.items():
            if pr == "RUN" or pr == "INITIALISING_DEFAULT" or pr == "INITIALIZE" or pr == 'config_file':
                pass
            else:
                if hasattr(cof,pr):
                    setattr(cof,pr,valu.replace("~'~'~",""))
    return cof

def hkmConfig(configClass:str):
    inbuildClass = {
        'App':App()
    }
    cof = None
    for nme,cl in inbuildClass.items():
        if nme == configClass:
            cof = __cfg__(cl)
    
    if not cof:
        cof = __import__(configClass, fromlist=[None])
    return cof  
        
                    
                
        