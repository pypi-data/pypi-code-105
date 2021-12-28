# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['umonitor']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'umonitor',
    'version': '0.1.2',
    'description': 'A package to run and monitor background services',
    'long_description': None,
    'author': 'Ruslan Sergeev',
    'author_email': 'mybox.sergeev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RuslanSergeev/uMonitor.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
