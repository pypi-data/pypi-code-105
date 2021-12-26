from .sqlee import SqleeRepository
from .config import __version__

__name__ = "sqlee"
__version__ = __version__
__all__ = [
    'connect', 'utils',
    ]
__author__ = "Entropy <fu050409@163.com>"
__incantation__ = "嗡嘛呢叭咪吽"

def connect(name=None, user=None, token=None, *args, **kwargs):
    if "owner" in kwargs or "repo" in kwargs:
        raise VersionError("该方式并非最新版本，")
    return SqleeRepository(access_token=token, repo=repo, owner=owner)
