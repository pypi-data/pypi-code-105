import abc

    


class ConfigSystemInterface(metaclass=abc.ABCMeta):
    """[summary]
    """
    
    
    @classmethod
    def __subclasshook__(cls,subclass)->bool:
        return (hasattr(subclass, 'Config') and 
                callable(subclass.Config) or
                NotImplemented
                )
        
    @abc.abstractmethod
    def Config(self,config:str):
        raise NotImplementedError
    