# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['automaton', 'automaton.actions', 'automaton.core']

package_data = \
{'': ['*']}

install_requires = \
['evdev>=1.4.0,<2.0.0', 'multiprocess>=0.70.12,<0.71.0']

setup_kwargs = {
    'name': 'automaton-linux',
    'version': '1.2.2',
    'description': 'An automation library for linux that uses UInput via evdev.',
    'long_description': None,
    'author': 'Abdul-Muiz-Iqbal',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
