from typing import Dict, List, Union, Tuple


class String:
    __SOURCE = {}
    __DEFAULT = 'it'
    
    def __init__(self, source = None, default = None, **kwargs):
        self.dict: Dict[str, str] = kwargs
        self.__SOURCE = source or String.__SOURCE
        self.__DEFAULT = default or String.__DEFAULT
    
    def result(self, language, args) -> str:
        result = self.dict.get(language, self.dict.get(self.__DEFAULT, 'Language Not Found'))
        return result.format(*args) if args else result
    
    def get(self, language, *args) -> str:
        lang_type = type(language)
        if lang_type != int and lang_type != str:
            language = self.__DEFAULT
        if type(language) != str:
            language = self.__SOURCE(language, self.__DEFAULT)
        return self.result(language, args)
    
    def __getitem__(self, args: Union[str, int, Tuple]) -> str:
        if type(args) == tuple:
            language, *args = args
        else:
            language, args = args, []
        lang_type = type(language)
        if lang_type != int and lang_type != str:
            language = self.__DEFAULT
        if type(language) != str:
            language = self.__SOURCE(language, self.__DEFAULT)
        return self.result(language, args)
    
    async def __call__(self, language, *args) -> str:
        lang_type = type(language)
        if lang_type != int and lang_type != str:
            language = self.__DEFAULT
        if type(language) != str:
            language = await self.__SOURCE(language, self.__DEFAULT)
        return self.result(language, args)
    
    def values(self) -> List[str]:  # fixme forse può restituire un set
        return list(self.dict.values())
    
    def set_source(self, source):
        if not callable(source):
            raise ValueError('Invalid source')
        self.__SOURCE = source
    
    def get_source(self):
        return self.__SOURCE
    
    def set_default(self, default: str = None):
        if default is None:
            default = String.__DEFAULT
        if type(default) != str:
            raise ValueError()
        self.__DEFAULT = default
    
    def get_default(self) -> str:
        return self.__DEFAULT
