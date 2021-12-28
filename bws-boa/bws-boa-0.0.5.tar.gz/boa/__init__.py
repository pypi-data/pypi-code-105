"""
    Builder Web Services
"""

from .core.bootstrap import bootstrap
from .core import urls
from .core import json
from .core import view
from .core import create_core
# from .core.cmd import create_app
# from .core.cmd import create_project


__version__ = "0.0.5"
__author__ = "Jose Angel Delgado"
__author_email__ = "esojangel@gmail.com"

__all__ = [
    "bootstrap",
    "urls",
    "json",
    "view",
    "create_core",
]
