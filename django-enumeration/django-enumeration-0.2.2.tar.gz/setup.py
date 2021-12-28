# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enumeration', 'enumeration.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2', 'django-enumfields==2.1.1']

setup_kwargs = {
    'name': 'django-enumeration',
    'version': '0.2.2',
    'description': 'Robust django enumeration sequences',
    'long_description': '============================\nDjango enumeration sequences\n============================\n\n**Consistent, gapless, periodic(optional) sequences with number formatting for accounting documents and such**\n\n\nRequirements\n==============\n\n* Postgres 9.5+\n* Python 3.6+\n\n\n\nInstallation\n____________\n\n1. pip install django-enumeration\n\n2. Add "enumeration" to your INSTALLED_APPS setting like this::\n\n    INSTALLED_APPS = [\n        ...\n        \'enumeration\',\n    ]\n\n3. Run `python manage.py migrate` to create the enumeration models.\n\n',
    'author': 'Mārtiņš Šulcs',
    'author_email': 'shulcsm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
