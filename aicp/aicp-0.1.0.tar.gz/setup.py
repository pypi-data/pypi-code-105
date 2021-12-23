# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aicp']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['aicp = aicp.main:app']}

setup_kwargs = {
    'name': 'aicp',
    'version': '0.1.0',
    'description': '',
    'long_description': '# AI Collaboration Platform',
    'author': 'Tobias Oberrauch',
    'author_email': 'tobias.oberrauch@pioneers.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
