# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['storage3', 'storage3.lib']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19,<0.22']

setup_kwargs = {
    'name': 'storage3',
    'version': '0.1.0',
    'description': 'Supabase Storage client for Python.',
    'long_description': '# Storage-py\n\nPython Client library to interact with Supabase Storage.\n',
    'author': 'Joel Lee',
    'author_email': 'joel@joellee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/supabase-community/storage-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
