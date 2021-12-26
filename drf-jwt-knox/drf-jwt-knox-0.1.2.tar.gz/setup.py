# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jwt_knox', 'jwt_knox.migrations']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'drf-jwt-knox',
    'version': '0.1.2',
    'description': 'Knox-fortified JSON Web Tokens for Django REST Framework',
    'long_description': "DRF JWT + Knox\n==============\n\n[![Build Status](https://travis-ci.org/ssaavedra/drf-jwt-knox.svg?branch=master)](https://travis-ci.org/ssaavedra/drf-jwt-knox)\n[![codecov](https://codecov.io/gh/ssaavedra/drf-jwt-knox/branch/master/graph/badge.svg)](https://codecov.io/gh/ssaavedra/drf-jwt-knox)\n[![PyPI version](https://img.shields.io/pypi/v/drf-jwt-knox.svg)](https://pypi.python.org/pypi/drf-jwt-knox)\n[![Requirements Status](https://requires.io/github/ssaavedra/drf-jwt-knox/requirements.svg?branch=master)](https://requires.io/github/ssaavedra/drf-jwt-knox/requirements/?branch=master)\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=ssaavedra_drf-jwt-knox&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=ssaavedra_drf-jwt-knox)\n\nThis package provides an authentication mechanism for Django REST\nFramework based on [JSON Web Tokens][JWT] in the browser backed up by\n[Knox][knox]-powered tokens in the database.\n\nThis package aims to take the better parts of both worlds, including:\n\n- Expirable tokens: The tokens may be manually expired in the\n  database, so a user can log out of all other logged-in places, or\n  everywhere.\n- Different tokens per login attempt (per user-agent), meaning that a\n  user's session is tied to the specific machine and logging can be\n  segregated per usage.\n- JWT-based tokens, so the token can have an embedded expiration time,\n  and further metadata for other applications.\n- Tokens are generated via OpenSSL so that they are cryptographically more secure.\n- Only the tokens' hashes are stored in the database, so that even if\n  the database gets dumped, an attacker cannot impersonate people\n  through existing credentials\n- Other applications sharing the JWT private key can also decrypt the JWT\n\n\nUsage\n=====\n\nAdd this application **and knox** to `INSTALLED_APPS` in your\n`settings.py`.\n\nThen, add this app's routes to some of your `urlpatterns`.\n\nYou can use the `verify` endpoint to verify whether a token is valid\nor not (which may be useful in a microservice architecture).\n\n\nTests\n=====\n\nTests are automated with `tox` and run on Travis-CI automatically. You\ncan check the status in Travis, or just run `tox` from the command\nline.\n\n\nContributing\n============\n\nThis project uses the GitHub Flow approach for contributing, meaning\nthat we would really appreciate it if you would send patches as Pull\nRequests in GitHub. If for any reason you prefer to send patches by email, they are also welcome and will end up being integrated here.\n\nLicense\n=======\n\nThis code is released under the Apache Software License Version 2.0.\n\n\n[JWT]: https://github.com/jpadilla/pyjwt\n[knox]: https://github.com/James1345/django-rest-knox\n",
    'author': 'Santiago Saavedra',
    'author_email': 'ssaavedra@gpul.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
