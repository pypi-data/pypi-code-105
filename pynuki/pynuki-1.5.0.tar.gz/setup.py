# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pynuki']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'pynuki',
    'version': '1.5.0',
    'description': 'Python bindings for nuki.io bridges',
    'long_description': '# pynuki\n\n![PyPI](https://img.shields.io/pypi/v/pynuki)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/pynuki)\n![PyPI - License](https://img.shields.io/pypi/l/pynuki)\n[![CI](https://github.com/pschmitt/pynuki/workflows/CI/badge.svg)](https://github.com/pschmitt/pynuki/actions?query=workflow%3A%22CI%22)\n\nPython library for interacting with Nuki locks and openers\n\n## Installation\n\n```bash\npip install -U pynuki\n```\n\n## Usage\n\n```python\nfrom pynuki import NukiBridge\n\nbridges = NukiBridge.discover()\nbr = bridges[0]\nbr.token = "YOUR_TOKEN"\n\n# Locks\nbr.locks[0].lock()\nbr.locks[0].unlock()\n\n# Openers\nbr.openers[0].activate_rto()\nbr.openers[0].deactivate_rto()\n```\n',
    'author': 'Philipp Schmitt',
    'author_email': 'philipp@schmitt.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pschmitt/pynuki',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.6,<4.0',
}


setup(**setup_kwargs)
