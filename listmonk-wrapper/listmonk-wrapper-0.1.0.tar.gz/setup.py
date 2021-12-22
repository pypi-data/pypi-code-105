# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['listmonk_wrapper', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

extras_require = \
{'dev': ['tox>=3.20.1,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0',
         'pip>=20.3.1,<21.0.0',
         'twine>=3.3.0,<4.0.0',
         'toml>=0.10.2,<0.11.0'],
 'test': ['black>=21.5b2,<22.0',
          'isort>=5.8.0,<6.0.0',
          'flake8>=3.9.2,<4.0.0',
          'pytest>=6.2.4,<7.0.0']}

setup_kwargs = {
    'name': 'listmonk-wrapper',
    'version': '0.1.0',
    'description': 'Light Python wrapper for listmonk.app.',
    'long_description': '# ListmonkWrapper\n\n\nLight Python wrapper for listmonk.app\n\n\n* PyPI: <https://pypi.org/project/ListmonkWrapper/>\n* Free software: BSD-3-Clause\n\n\n## Features\n\n* `pip install listmonk_wrapper`\n',
    'author': 'Michael McClelland',
    'author_email': 'mmcclelland@thesummitgrp.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Lenders-Cooperative/ListmonkWrapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
