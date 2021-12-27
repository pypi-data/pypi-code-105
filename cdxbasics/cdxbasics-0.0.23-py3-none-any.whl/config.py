"""
config
Utility object for ML project configuration
Hans Buehler 2021
"""

from collections import OrderedDict
from .logger import Logger
_log = Logger(__file__)

class Config(OrderedDict):
    """
        A simple Config class.
        Main features
        
        Write
            Set data as usual:
            
                config = Config()
                config['features']           = [ 'ime', 'spot' ]
                config['weights']            = [ 1, 2, 3 ]
                
            Create sub configuration
            
                config.network['samples']    = 10000
                config.network['activation'] = 'relu'
                
        Read
            def read_config( confg ):
            
                features = config("features", [], list )          # reads features and returns a list
                weights  = config("weights", [], np.ndarray )     # reads features and returns a nump array
                
                network  = config.network
                samples  = network('samples', 10000)              # networks samples
                network.done()                                    # returns an error as we haven't read 'activitation'

        Attributes
        ----------
            Can access any sub config.

    """
    
    No_Default = [[None]]
    
    def __init__(self, **kwargs):
        OrderedDict.__init__(self)
        self._read    = set()
        self._path    = "Config"
        self._configs = OrderedDict()
        self.update(kwargs)
        
    # config management
    # -----------------
    
    def is_empty(self) -> bool:
        """ Checks whether any variables have been set """
        return len(self) == 0
    
    def done(self, include_sub_configs : bool = True ):
        """ Closes the config and checks that no unread parameters remain.
        """
        inputs = set(self)
        rest   = inputs - self._read
        _log.verify( len(rest) == 0, "Error closing config '%s': the following config arguments were not read: %s", self._path, list(rest))
        
        if include_sub_configs:
            for config in self._configs:
                self._configs[config].done()
        return
    
    def mark_done(self):
        """ Announce all data was read correctly """
        self._read = set( self )        

    def __getattr__(self, key : str):
        """ Returns a config with name 'key' """
        _log.verify( key.find('.') == -1 and key.find(" ") == -1, "Error in config '%s': name of a config must be a valid class member name. Found %s", self._path, key )
        if key in self._configs:
            return self._configs[key]
        config = Config()
        config._path = self._path + "." + key
        self._configs[key] = config
        return config

    def copy(self,  mark_done : bool = True ):
        """ Create a copy of this config.
        
            Parameters
            ----------
                mark_done : bool, optional 
                    If true mark the current object as 'read'. 
                    This way we can store a sub config for later processing
                    with triggering a warning with self.done()
        
        """
        config = Config()
        config.update(self)
        config._read    = set( self._read )
        config._path    = self._path
        config._configs = OrderedDict( self._configs )
        if mark_done:
            self.mark_done()
        return config
        
    # Read
    # -----
        
    def __call__(self, key : str, *kargs ):
        """ Reads 'key' from the config. If not found, return 'default' if specified.
        
                config("key")                      - returns the value for 'key' or if not found raises an exception
                config("key", 1)                   - returns the value for 'key' or if not found returns 1
                config("key", 1, int)              - if 'key' is not found, return 1. If it is found cast the result with int().
        
            Parameters
            ----------
                key : string
                    Keyword to read
                args : list, optional
                    First argument is the default value. Second argument is the desired instance type
                    
            Returns
            -------
                Value.
        """        
        _log.verify( len(kargs) <= 2, "Error in config '%s': can only handle up to three arguments, including 'key'", self._path)
        
        if not key in self:
            if len(kargs) == 0:
                raise KeyError(key, "Error in config '%s': key '%s' not found " % (self._path, key))
            value = kargs[0]
        else:
            value = OrderedDict.get(self,key)
        if not value is None and len(kargs) == 2:
            try:
                value = kargs[1]( value )
            except Exception as e:
                _log.verify( False, "Error in config '%s': value '%s' for key '%s' cannot be cast to type '%s': %s", self._path, value, key, kargs[1].__name__, str(e))
        # mark key as read
        self._read.add(key)
        return value
        
    def __getitem__(self, key : str):
        """" Returns self(key) """
        return self(key)
    def get(self, key : str):
        """" Returns self(key) """
        return self(key)
    def get_default(self, key : str, default):
        """" Returns self(key,default) """
        return self(key,default)
    