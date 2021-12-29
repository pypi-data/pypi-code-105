# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['meta_memcache', 'meta_memcache.base']

package_data = \
{'': ['*']}

install_requires = \
['uhashring>=2.1,<3.0']

setup_kwargs = {
    'name': 'meta-memcache',
    'version': '0.1.0',
    'description': 'Modern, pure python, memcache client with support for new meta commands.',
    'long_description': '# meta-memcache-py\nModern, pure python, memcache client with support for new meta commands.\n',
    'author': 'Guillermo Perez',
    'author_email': 'bisho@revenuecat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
