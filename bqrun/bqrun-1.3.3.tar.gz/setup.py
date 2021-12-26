# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bqrun']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0', 'networkx>=2.6.3,<3.0.0', 'pydot>=1.4.2,<2.0.0']

entry_points = \
{'console_scripts': ['bqrun = bqrun.cli:main']}

setup_kwargs = {
    'name': 'bqrun',
    'version': '1.3.3',
    'description': 'Query runner for BigQuery. It automatically analyzes dependencies and runs only necessary queries in parallel.',
    'long_description': '=====\nbqrun\n=====\n\n\n.. image:: https://img.shields.io/pypi/v/bqrun.svg\n        :target: https://pypi.python.org/pypi/bqrun\n\n.. image:: https://img.shields.io/travis/hotoku/bqrun.svg\n        :target: https://travis-ci.com/hotoku/bqrun\n\n.. image:: https://readthedocs.org/projects/bqrun/badge/?version=latest\n        :target: https://bqrun.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\n\na\n\n\n* Free software: MIT license\n* Documentation: https://bqrun.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n',
    'author': 'Yasunori Horikoshi',
    'author_email': 'horikoshi.et.al@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hotoku/bqrun',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
