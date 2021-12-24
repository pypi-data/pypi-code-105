# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yeouia', 'yeouia.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2']

setup_kwargs = {
    'name': 'yeouia',
    'version': '3.0.0',
    'description': 'Yummy Email Or Username Insensitive Auth model backend for Django',
    'long_description': "# Yummy Email Or Username Insensitive Auth model backend for Django\n\n[![PyPI version](https://badge.fury.io/py/django-yeouia.svg)](https://pypi.org/project/django-yeouia)\n[![Tests](https://github.com/nim65s/django-YummyEmailOrUsernameInsensitiveAuth/actions/workflows/test.yml/badge.svg)](https://github.com/nim65s/django-YummyEmailOrUsernameInsensitiveAuth/actions/workflows/test.yml)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/nim65s/django-YummyEmailOrUsernameInsensitiveAuth/master.svg)](https://results.pre-commit.ci/latest/github/nim65s/django-YummyEmailOrUsernameInsensitiveAuth/master)\n[![codecov](https://codecov.io/gh/nim65s/django-YummyEmailOrUsernameInsensitiveAuth/branch/master/graph/badge.svg?token=APCEYTJRV3)](https://codecov.io/gh/nim65s/django-YummyEmailOrUsernameInsensitiveAuth)\n[![Maintainability](https://api.codeclimate.com/v1/badges/6737a84239590ddc0d1e/maintainability)](https://codeclimate.com/github/nim65s/django-YummyEmailOrUsernameInsensitiveAuth/maintainability)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n## Instructions\n\n1. `pip install django-yeouia`\n2. Add `AUTHENTICATION_BACKENDS = ['yeouia.backends.YummyEmailOrUsernameInsensitiveAuth']` to your `settings.py`\n3. Enjoy\n\n## Requirements\n\nTested for\n\n* Python 3.8, 3.9\n* Django 2.2+\n\nMay work otherwise, but you should run tests :P\n\n## Case Insensitive ?\n\nDjango's default auth username is *not* case insensitive.\n(See [#2273](https://code.djangoproject.com/ticket/2273) and [#25617](https://code.djangoproject.com/ticket/25617))\n\nBut… Who cares ?\n\nThis backend tries:\n\n1. username, case sensitive\n2. username, case insensitive\n3. email, case insensitive\n\nAnd follows [#20760](https://code.djangoproject.com/ticket/20760).\n",
    'author': 'Guilhem Saurel',
    'author_email': 'guilhem.saurel@laas.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nim65s/django-YummyEmailOrUsernameInsensitiveAuth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
