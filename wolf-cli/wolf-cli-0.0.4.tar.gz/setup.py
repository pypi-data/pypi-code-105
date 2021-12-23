# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wolf_cli', 'wolf_cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=3.4.0,<4.0.0',
 'click>=8.0.3,<9.0.0',
 'httpx>=0.21.1,<0.22.0',
 'rich>=10.16.1,<11.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['wolf = wolf_cli.cli:app']}

setup_kwargs = {
    'name': 'wolf-cli',
    'version': '0.0.4',
    'description': 'CLI tool to assist and make easy repetitive tasks such as downloading images and URLs unshortening',
    'long_description': '[![PyPi version](https://badgen.net/pypi/v/wolf-cli)](https://pypi.com/project/wolf-cli)\n\n# **Wolf**\n## A CLI tool to assist and make easy repetitive tasks such as downloading images and URLs unshortening\n\n### Built with:\n- [Poetry](https://python-poetry.org/)\n- [Typer](https://typer.tiangolo.com/)\n---\nThis Project uses code adapted from: [Kevin Tewouda](https://lewoudar.medium.com/click-a-beautiful-python-library-to-write-cli-applications-9c8154847066)\n',
    'author': 'cande1gut',
    'author_email': 'candelario.gtz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cande1gut/wolf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
