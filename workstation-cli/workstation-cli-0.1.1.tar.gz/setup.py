# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['workstation']

package_data = \
{'': ['*'], 'workstation': ['resources/*', 'resources/zshrc/*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'distro>=1.6.0,<2.0.0',
 'loguru==0.5.3',
 'wget>=3.2,<4.0']

entry_points = \
{'console_scripts': ['install-workstation = '
                     'workstation.cli:install_workstation']}

setup_kwargs = {
    'name': 'workstation-cli',
    'version': '0.1.1',
    'description': 'Python lib for my personal workstation setup',
    'long_description': '# Workstation\n\n![Tests](https://github.com/militu/workstation/actions/workflows/tests.yml/badge.svg)\n![Docs](https://github.com/militu/workstation/actions/workflows/documentation.yml/badge.svg)\n\n### 🕮 Documentation\n\nFor detailed documentation (todo), please see [here](https://militu.github.io/workstation/)\n\n```shell\npip install workstation --user\n```\n\n### \U0001fa9b Develop\n\nFirst install workstation\n\n```shell\npyenv install -s 3.8.12\npyenv local 3.8.12\npoetry lock\nnox -s pre-commit -- install\nnox -s pre-commit -- install --hook-type commit-msg\n```\n\nRelease\n\n```shell\ngit switch --create release main\nnox -s release -- --patch\ngit push origin release\n```\n',
    'author': 'Victor Mazzeo',
    'author_email': 'victor.mazzeo@groupeseloger.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/militu/workstation-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
