# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfreetts']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyfreetts',
    'version': '0.1.0',
    'description': 'Convert text to speech with the pretty voices',
    'long_description': '# pyfreetts\n\n<p align="center"><a href="https://codecov.io/github/tquangsdh20/pyfreetts/commit/5d0da7ae595f845c64742d9d64260d7018453856"><img src="https://codecov.io/gh/tquangsdh20/pyfreetts/branch/master/graphs/badge.svg?branch=master"></a></p>\n\nConvert text to speech with the FreeTTS API &amp; VoiceMarker\n\n',
    'author': 'Joseph Quang',
    'author_email': 'tquangsdh20@fsob.win',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tquangsdh20/pyfreetts',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
