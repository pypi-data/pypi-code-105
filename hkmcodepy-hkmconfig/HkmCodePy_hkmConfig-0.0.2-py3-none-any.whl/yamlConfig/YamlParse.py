import yaml

class YamlParse:
    
    def __init__(self) -> None:
        self.pathToYamlSource = None
        self.data = None
    def Yes(self):
        print("yes....")
    def GET(self, yamlSource:str):
        self.SET_YAML_SOURCE(yamlSource)
        self._PARSING_YAML()
        return self.data
    
    def SET_YAML_SOURCE(self, source:str)->None:
        if not source.strip():
            raise FileNotFoundError
        else:
            self.pathToYamlSource = source
            
    
    def _PARSING_YAML(self)->None:
        if not self.pathToYamlSource:
            raise FileNotFoundError
        else:
            with open(self.pathToYamlSource,'r') as yamlFile:
                try:
                    config = yaml.load(yamlFile, Loader=yaml.FullLoader)
                    self.data = config
                except yaml.YAMLError as exc:
                    print(exc)
                
                
        
        
        
        