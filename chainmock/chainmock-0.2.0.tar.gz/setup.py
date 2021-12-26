# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['chainmock']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.0.0']

entry_points = \
{'pytest11': ['chainmock = chainmock._pytest_plugin']}

setup_kwargs = {
    'name': 'chainmock',
    'version': '0.2.0',
    'description': 'Mocking library for Python and Pytest',
    'long_description': '# Chainmock\n\n<a href="https://pypi.org/project/chainmock/">\n  <img src="https://img.shields.io/pypi/v/chainmock" alt="pypi">\n</a>\n<a href="https://github.com/ollipa/chainmock/actions/workflows/ci.yml">\n  <img src="https://github.com/ollipa/chainmock/actions/workflows/ci.yml/badge.svg" alt="ci">\n</a>\n<a href="https://chainmock.readthedocs.io/">\n  <img src="https://img.shields.io/readthedocs/chainmock" alt="documentation">\n</a>\n<a href="./LICENSE">\n  <img src="https://img.shields.io/pypi/l/chainmock" alt="license">\n</a>\n\nMocking library for Python and Pytest.\n\n## Documentation\n\nhttps://chainmock.readthedocs.io/\n',
    'author': 'Olli Paakkunainen',
    'author_email': 'olli@paakkunainen.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ollipa/chainmock',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
