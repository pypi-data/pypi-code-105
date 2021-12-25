# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miniseed2mat']

package_data = \
{'': ['*']}

install_requires = \
['obspy>=1.2.2,<2.0.0', 'scipy>=1.7.3,<2.0.0']

entry_points = \
{'console_scripts': ['mseed2mat = miniseed2mat.main:convertmseed2mat']}

setup_kwargs = {
    'name': 'miniseed2mat',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Utpal Kumar',
    'author_email': 'utpalkumar50@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
