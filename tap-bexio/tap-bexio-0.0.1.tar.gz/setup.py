# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_bexio', 'tap_bexio.tests']

package_data = \
{'': ['*'], 'tap_bexio': ['schemas/*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk>=0.3.17,<0.4.0']

entry_points = \
{'console_scripts': ['tap-bexio = tap_bexio.tap:Tapbexio.cli']}

setup_kwargs = {
    'name': 'tap-bexio',
    'version': '0.0.1',
    'description': '`tap-bexio` is a Singer tap for bexio, built with the Meltano SDK for Singer Taps.',
    'long_description': None,
    'author': 'Nino Müller',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<3.11',
}


setup(**setup_kwargs)
