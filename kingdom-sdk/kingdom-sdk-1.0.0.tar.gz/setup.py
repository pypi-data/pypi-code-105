# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kingdom_sdk',
 'kingdom_sdk.adapters',
 'kingdom_sdk.database',
 'kingdom_sdk.domain',
 'kingdom_sdk.ports',
 'kingdom_sdk.utils']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.25,<2.0.0',
 'jinjasql>=0.1.8,<0.2.0',
 'pytz>=2021.3,<2022.0',
 'redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'kingdom-sdk',
    'version': '1.0.0',
    'description': 'Library containing the core modules for the kingdom-python-server',
    'long_description': '# 🏰 Kingdom SDK\n\nLibrary containing the core modules for the kingdom-python-server.\n\n## Features\n\nSee the [changelog](./CHANGELOG.md) to see all the features supported.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install `kingdom-sdk`.\n\n```bash\npip install kingdom-sdk\n```\n\nYou can use [poetry](https://python-poetry.org/) as well.\n\n```bash\npoetry add kingdom-sdk\n```\n\n## Usage\n\n```python\nfrom kingdom_sdk.utils import files\n\norm_files = files.find("orm.py", "/")\n```\n\n## Test\n\nTo test the database package, you need do it manually, running a migration. Make sure the database is configured before.\n\n```bash\ncd tests/poc/\nalembic revision --autogenerate\nalembic upgrade head\n```\n\nThe rest, run `pytest`.\n\nDon\'t commit the generated revision.\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'William Abreu',
    'author_email': 'william@t10.digital',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
