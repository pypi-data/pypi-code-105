# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_storage_supabase']

package_data = \
{'': ['*']}

install_requires = \
['supabase>=0.0.3,<0.0.4']

setup_kwargs = {
    'name': 'django-storage-supabase',
    'version': '0.1.0',
    'description': 'Package for using Supabase Storage as a custom storage backend',
    'long_description': None,
    'author': 'Joel Lee',
    'author_email': 'joel@joellee.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
