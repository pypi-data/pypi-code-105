# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sauth']
install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['sauth = sauth:main']}

setup_kwargs = {
    'name': 'sauth',
    'version': '1.1.0',
    'description': 'simple server for serving directories via http or https and BASIC authorization',
    'long_description': '=====\nsauth\n=====\n\n\n.. image:: https://img.shields.io/pypi/v/sauth.svg\n        :target: https://pypi.python.org/pypi/sauth\n\n**S** erver **auth**\n\nA simple server for serving directories via http or https and BASIC authorization::\n\n    $ sauth --help\n    Usage: sauth [OPTIONS] USERNAME PASSWORD [IP] [PORT]\n\n      Start http server with basic authentication current directory.\n\n    Options:\n      -d, --dir TEXT  use different directory\n      -s, --https     use https\n      -t, --thread    serve each request in a different thread\n      --help          Show this message and exit.\n\n* Free software: GNU General Public License v3\n\nInstallation\n------------\n\n::\n\n    pip install sauth\n\nAlso available on Arch User Repository if you\'re running arch::\n    \n    pacaur -S sauth\n\nUsage\n-----\n\nTo serve your current directory simply run::\n\n    $ sauth someuser somepass\n    Serving "/home/user/somedir" directory on http://0.0.0.0:8333\n\nYou can specify port and ip to serve on with 3rd and 4th arguments::\n\n    $ sauth someuser somepass 127.0.0.1 1234\n    Serving "/home/user/somedir" directory on http://127.0.0.1:1234\n\nThreading is also supported through `-t` or `--thread` flags:\n\n    $ sauth someuser somepass 127.0.0.1 1234 --thread\n    Serving "/home/user/somedir" directory on http://127.0.0.1:1234 using threading',
    'author': 'granitosaurus',
    'author_email': 'bernardas.alisauskas@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Granitosaurus/sauth/',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
