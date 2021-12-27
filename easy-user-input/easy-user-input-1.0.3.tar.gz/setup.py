# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easy_user_input']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'easy-user-input',
    'version': '1.0.3',
    'description': 'Misc python3 methods for collecting input from users',
    'long_description': '# easy-user-input\nMiscellaneous python3 methods for collecting input from users\n\nCreated for use in a different project.\n',
    'author': 'generic-user1',
    'author_email': '89677116+generic-user1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
