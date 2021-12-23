# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sismoscl']

package_data = \
{'': ['*'],
 'sismoscl': ['.github/*', '.github/ISSUE_TEMPLATE/*', '.github/workflows/*']}

install_requires = \
['rich>=10.14.0,<11.0.0', 'typer[all]>=0.4.0,<0.5.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=4.5.0,<5.0.0']}

entry_points = \
{'console_scripts': ['sismoscl = sismoscl.__main__:app']}

setup_kwargs = {
    'name': 'sismoscl',
    'version': '0.1.1',
    'description': 'Sismos ocurridos en Chile, casi en tiempo real',
    'long_description': '# sismoscl\n\n<div align="center">\n\n\n[![Python Version](https://img.shields.io/pypi/pyversions/sismoscl.svg)](https://pypi.org/project/sismoscl/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/fraediaz/sismoscl/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/fraediaz/sismoscl/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/fraediaz/sismoscl/releases)\n[![License](https://img.shields.io/github/license/fraediaz/sismoscl)](https://github.com/fraediaz/sismoscl/blob/master/LICENSE)\n![Coverage Report](assets/images/coverage.svg)\n\nSismos ocurridos en Chile, casi en tiempo real\n\n</div>\n\n\n### Instalación\n\nCon python >= 3.7\n\n```bash\npip install -U sismoscl\n```\n\n### Configuración\n\nImporta la librería, luego su función\n\n```bash\nfrom sismoscl import sismos\n```\n\n\n### Uso\n\nDevuelve una lista con los últimos sismos registrados por la Universidad de Chile\n```bash\nsismos()\n```\n\nDevuelve una lista con los últimos sismos mayores a magnitud 2\n```bash\nsismos(2)\n```',
    'author': 'fraediaz',
    'author_email': 'fraediaz@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fraediaz/sismoscl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
