# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastack',
 'fastack.plugins',
 'fastack.plugins.aioredis',
 'fastack.plugins.mongoengine',
 'fastack.plugins.sqlmodel',
 'fastack.templates.app',
 'fastack.templates.app.commands',
 'fastack.templates.app.controllers',
 'fastack.templates.app.controllers.dummy',
 'fastack.templates.app.plugins',
 'fastack.templates.app.settings']

package_data = \
{'': ['*'], 'fastack': ['templates/*']}

install_requires = \
['asgi-lifespan>=1.0.1,<2.0.0',
 'fastapi>=0.70.1,<0.71.0',
 'typer[all]>=0.4.0,<0.5.0',
 'uvicorn>=0.16.0,<0.17.0']

extras_require = \
{'nosql': ['mongoengine>=0.23.1,<0.24.0'],
 'redis': ['aioredis>=2.0.0,<3.0.0'],
 'sql': ['sqlmodel>=0.0.5,<0.0.6']}

entry_points = \
{'console_scripts': ['fastack = fastack.cli:fastack']}

setup_kwargs = {
    'name': 'fastack',
    'version': '2.0.0',
    'description': 'Fastack is a blah blah blah framework!!!',
    'long_description': "# Fastack\n\nfastack is a blah blah blah framework, for creating clean and easy-to-manage REST API project structures. It's built for FastAPI framework ❤️\n\nThe goals of this project are:\n\n* Create a clean and easy-to-manage REST API project structure\n* Create a REST API with our ``Controller`` class\n* Include pagination\n* Support adding own commands using the ``typer`` library\n* Integrated with docker & docker-compose\n* Integrated with pre-commit tool\n\n\n# Installation\n\n```\npip install fastack\n```\n\n# Example\n\ncreate project structure\n\n```\nfastack new awesome-project\ncd awesome-project\n```\n\ninstall pipenv & create virtual environment\n\n```\npip install pipenv && pipenv install && pipenv shell\n```\n\nrun app\n\n```\nfastack runserver\n```\n\n# Documentation\n\nSorry in advance, for the documentation I haven't had time to make it 🙏\n",
    'author': 'aprilahijriyan',
    'author_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'maintainer': 'aprilahijriyan',
    'maintainer_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'url': 'https://github.com/fastack-dev/fastack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
