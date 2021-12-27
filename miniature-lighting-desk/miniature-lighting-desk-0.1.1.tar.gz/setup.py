# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miniature_lighting_desk']

package_data = \
{'': ['*']}

install_requires = \
['autobahn[serialization]>=21.11.1,<22.0.0',
 'click>=8.0.3,<9.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'pyusb>=1.2.1,<2.0.0']

entry_points = \
{'console_scripts': ['lighting_desk = miniature_lighting_desk.cli:cli']}

setup_kwargs = {
    'name': 'miniature-lighting-desk',
    'version': '0.1.1',
    'description': 'Desk software for Miniature Lighting Controller',
    'long_description': None,
    'author': 'John Maximilian',
    'author_email': '2e0byo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
