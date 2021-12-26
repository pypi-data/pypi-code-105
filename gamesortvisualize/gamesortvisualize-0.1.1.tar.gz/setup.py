# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gamesortvisualize']

package_data = \
{'': ['*']}

install_requires = \
['pygame>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'gamesortvisualize',
    'version': '0.1.1',
    'description': 'A Sorting Visualizer for Sorting Algorithms',
    'long_description': '# gamesortvisualize\nvisualizer for sorting algorithms using pygame \n',
    'author': 'sakthiRatnam',
    'author_email': 'sakthiratnam050@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sakthiRathinam/gamesortvisualize',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
