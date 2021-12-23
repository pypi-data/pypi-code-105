# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_zohosprints', 'tap_zohosprints.tests']

package_data = \
{'': ['*'], 'tap_zohosprints': ['schemas/*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk==0.3.17']

entry_points = \
{'console_scripts': ['tap-zohosprints = '
                     'tap_zohosprints.tap:TapZohoSprints.cli']}

setup_kwargs = {
    'name': 'tap-zohosprints',
    'version': '0.0.4',
    'description': '`tap-zohosprints` is a Singer tap for ZohoSprints, built with the Meltano SDK for Singer Taps.',
    'long_description': None,
    'author': 'AutoIDM',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<=3.10',
}


setup(**setup_kwargs)
