from .sqlee import SqleeRepository
from .config import __version__
from .utils.exceptions import VersionError

__name__ = "sqlee"
__version__ = __version__
__all__ = [
    'connect', 'utils',
    ]
__author__ = "Entropy <fu050409@163.com>"
__incantation__ = "嗡嘛呢叭咪吽"

def connect(name=None, user=None, token=None, *args, **kwargs):
    if "owner" in kwargs or "repo" in kwargs:
        raise VersionError("该连接数据库方式已在2.0.0版本后被弃用.")
    return SqleeRepository(access_token=token, repo=name, owner=user, *args, **kwargs)
