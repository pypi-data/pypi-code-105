# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netspeedlogger', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['altair>=4.1.0,<5.0.0',
 'fire==0.4.0',
 'pandas>=1.3.5,<2.0.0',
 'speedtest-cli>=2.1.3,<3.0.0',
 'streamlit>=1.3.0,<2.0.0',
 'tabulate>=0.8.9,<0.9.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-material>=6.1.7,<7.0.0',
         'mkdocstrings>=0.13.6,<0.14.0',
         'mkdocs-autorefs==0.1.1'],
 'test': ['black==20.8b1',
          'isort==5.6.4',
          'flake8==3.8.4',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest==6.1.2',
          'pytest-cov==2.10.1']}

entry_points = \
{'console_scripts': ['netspeedlogger = netspeedlogger.cli:main']}

setup_kwargs = {
    'name': 'netspeedlogger',
    'version': '0.1.0',
    'description': 'A python library for keeping track of your internet speed over time.',
    'long_description': '# Internet Speed Test Logger\n\n\n<p align="center">\n<a href="https://pypi.python.org/pypi/netspeedlogger">\n    <img src="https://img.shields.io/pypi/v/netspeedlogger.svg"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/radinplaid/netspeedlogger/actions">\n    <img src="https://github.com/radinplaid/netspeedlogger/actions/workflows/main.yml/badge.svg?branch=release" alt="CI Status">\n</a>\n\n<a href="https://netspeedlogger.readthedocs.io/en/latest/?badge=latest">\n    <img src="https://readthedocs.org/projects/netspeedlogger/badge/?version=latest" alt="Documentation Status">\n</a>\n\n</p>\n\n\nA python library for keeping track of your internet speed over time\n\n\n* Free software: MIT\n* Documentation: <https://netspeedlogger.readthedocs.io>\n\n\n## Features\n\n* Easily test your internet speed with (speedtest-cli)[https://github.com/sivel/speedtest-cli]\n* Keep track of your internet speed over time\n* (Streamlit)[https://streamlit.io/] application for visualizing results\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [zillionare/cookiecutter-pypackage](https://github.com/zillionare/cookiecutter-pypackage) project template.\n',
    'author': 'Mark Franey',
    'author_email': 'franey.mark@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/radinplaid/netspeedlogger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
