# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['impressive_strawberry',
 'impressive_strawberry.database',
 'impressive_strawberry.database.alembic',
 'impressive_strawberry.database.alembic.versions',
 'impressive_strawberry.web',
 'impressive_strawberry.web.crud',
 'impressive_strawberry.web.deps',
 'impressive_strawberry.web.errors',
 'impressive_strawberry.web.handlers',
 'impressive_strawberry.web.models',
 'impressive_strawberry.web.responses',
 'impressive_strawberry.web.routes',
 'impressive_strawberry.web.routes.api.achievement.v1',
 'impressive_strawberry.web.routes.api.application.v1',
 'impressive_strawberry.web.routes.api.group.v1',
 'impressive_strawberry.web.routes.api.unlock.v1',
 'impressive_strawberry.web.routes.api.user.v1',
 'impressive_strawberry.web.testing',
 'impressive_strawberry.webhooks']

package_data = \
{'': ['*'], 'impressive_strawberry.web': ['templates/*']}

install_requires = \
['SQLAlchemy>=1.4.26,<2.0.0',
 'alembic>=1.7.4,<2.0.0',
 'fastapi>=0.70.0,<0.71.0',
 'httpx>=0.21.1,<0.22.0',
 'lazy-object-proxy>=1.6.0,<2.0.0',
 'psycopg2-binary>=2.9.1,<3.0.0',
 'pytest-cov>=3.0.0,<4.0.0',
 'python-dotenv>=0.19.1,<0.20.0',
 'uvicorn>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'impressive-strawberry',
    'version': '0.1.1',
    'description': 'Achievements-as-a-service',
    'long_description': '# Strawberry\n\nAchievements-as-a-service\n\n## Design docs\n\nDesign docs are available on [FigJam](https://www.figma.com/file/8J7exqW3srh0WNiICHnf0O/Medals?node-id=0%3A1).\n',
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': 'Stefano Pigozzi',
    'maintainer_email': 'me@steffo.eu',
    'url': 'https://impressive-strawberry.ryg.one/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
