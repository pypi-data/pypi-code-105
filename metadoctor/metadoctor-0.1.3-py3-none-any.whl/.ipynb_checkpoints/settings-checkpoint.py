__all__ = [
    'Settings',
]

import os
from collections import ChainMap
from starlette.config import Config
from starlette.datastructures import Secret, CommaSeparatedStrings
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from dataclasses import dataclass, field



WORKING_DIRECTORY = os.getcwd()
ENV_FILE = os.path.abspath('.env')

static = StaticFiles(directory=os.path.join(WORKING_DIRECTORY, 'static'))
jinja = Jinja2Templates(directory=os.path.join(WORKING_DIRECTORY, 'templates'))
config = Config(env_file=ENV_FILE)



@dataclass
class Settings:
    config: Config = config
    static: StaticFiles = static 
    jinja: Jinja2Templates = jinja
        
    def __post_init__(self):
        self.chain = ChainMap({}, {k: Secret(v) for k,v in vars(self.config)['file_values'].items()})
        
    @property
    def cwd(self):
        return os.getcwd()
    
    @property
    def env_file(self):
        return os.path.abspath('.env')

    def update(self, data: dict):
        self.chain.update(data)

    def get(self, key):
        return Secret(self.chain.get(key))
    
    def all_chain(self):
        return self.chain
    
    def initial(self):
        return {k:Secret(v) for k,v in self.chain.maps[-1].items()}    
    