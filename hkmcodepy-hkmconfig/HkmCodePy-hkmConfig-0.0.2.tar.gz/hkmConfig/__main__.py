from ConfigSystemInterfaces import ConfigSystemInterface
from autoload import ModuleLoader

from NamespaceHelpers import hkmConfig

loader = ModuleLoader()
loader.load_classes("./", recursive=True)

class ConfigSystem(ConfigSystemInterface):
    def __init__(self) -> None:
        self.currentConfig = None
        
    def Config(self,config):
        self.currentConfig = hkmConfig(config)
        return self.currentConfig
    def GetCurrentConfig(self):
        return self.currentConfig


        
if __name__ == "__main__":
    # Examples:
    #  1  coff = hkmConfig('App')
    #     print(coff.baseURL)
    # 
    # 
    #  2  config = ConfigSystem()
    #     coff = config.Config('App')
    #     print(coff.baseURL)
    
    pass