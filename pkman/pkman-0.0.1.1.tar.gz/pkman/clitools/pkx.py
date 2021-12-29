import os
import sys
from .utils import CmdUtil,IoUtil
from .config import PACKGAE_CONFIG_FILENAME
os.environ['ANSI_COLORS_DISABLED']="1"
import fire
from . import apis

def load_pkg_info():
    pkg_info = IoUtil.json_load(os.path.join(os.getcwd(), PACKGAE_CONFIG_FILENAME))
    return pkg_info
class TYPES:
    class WEB_FILE:
        pass
    class GIT_FILE:
        pass
    class PACKAGE:
        pass
def complete_address():
    pass
def guess_type(address:str):
    if address.startswith('http://') or address.startswith('https://'):
        return TYPES.WEB_FILE


def pkx(address: str, *args, **kwargs):
    type=guess_type(address)
    if type is TYPES.WEB_FILE:
        pass
    elif type is TYPES.GIT_FILE:
        pass
    elif type is TYPES.PACKAGE:
        pass



def main():
    fire.Fire(pkx)

if __name__ == '__main__':
    main()