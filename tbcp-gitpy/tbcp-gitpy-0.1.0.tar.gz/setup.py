# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tbcp_gitpy', 'tbcp_gitpy.helpers']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.24,<4.0.0']

setup_kwargs = {
    'name': 'tbcp-gitpy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'John Ollhorn',
    'author_email': 'john@ollhorn.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
