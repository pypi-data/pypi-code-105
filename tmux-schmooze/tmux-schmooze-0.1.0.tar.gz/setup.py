# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tmux_schmooze']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'fuzzyfinder>=2.1.0,<3.0.0', 'textual>=0.1.12,<0.2.0']

setup_kwargs = {
    'name': 'tmux-schmooze',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Cam Graff',
    'author_email': 'graffcameron@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
