# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rhizo_widgets']

package_data = \
{'': ['*']}

install_requires = \
['ipywidgets>=7.6.5,<8.0.0']

setup_kwargs = {
    'name': 'rhizo-widgets',
    'version': '0.1.12',
    'description': '',
    'long_description': None,
    'author': 'Andy Jefferson',
    'author_email': 'andy@rhizo.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
