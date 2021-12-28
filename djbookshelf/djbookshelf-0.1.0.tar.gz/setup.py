# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djbookshelf', 'djbookshelf.migrations']

package_data = \
{'': ['*'], 'djbookshelf': ['templates/djbookshelf/*']}

install_requires = \
['django-bootstrap-v5>=1.0.7,<2.0.0', 'django>=3.2,<5', 'requests>=2,<3']

setup_kwargs = {
    'name': 'djbookshelf',
    'version': '0.1.0',
    'description': '',
    'long_description': '# django-template\n\nMy personal Django template project.\n\nThis a blank django template for my project. Build\naround [this post](https://victoria.dev/blog/my-django-project-best-practices-for-happy-developers/) and other find\nonline.\n',
    'author': 'Fundor333',
    'author_email': 'fundor333@fundor333.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://djbookshelf.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
