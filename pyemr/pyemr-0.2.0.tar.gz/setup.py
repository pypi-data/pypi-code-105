# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyemr', 'pyemr.files.templates', 'pyemr.utils']

package_data = \
{'': ['*'], 'pyemr': ['docker/*', 'files/*', 'kernals/*', 'sh/*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'autocorrect>=2.6.1,<3.0.0',
 'autopep8>=1.6.0,<2.0.0',
 'awswrangler>=2.0.0,<3.0.0',
 'boto3>=1.20.23,<2.0.0',
 'brunette>=0.2.2,<0.3.0',
 'cron-descriptor>=1.2.24,<2.0.0',
 'datefinder>=0.7.1,<0.8.0',
 'fire>=0.4.0,<0.5.0',
 'loguru>=0.5.3,<0.6.0',
 'numpy==1.18.0',
 'pandas>=1.1.0,<2.0.0',
 'poetry>=1.1.12,<2.0.0',
 'pylint>=2.12.2,<3.0.0',
 'sh>=1.14.2,<2.0.0',
 'tomlkit==0.7.2',
 'tqdm>=4.62.3,<5.0.0']

entry_points = \
{'console_scripts': ['pyemr = pyemr.cli:main']}

setup_kwargs = {
    'name': 'pyemr',
    'version': '0.2.0',
    'description': 'A lightweight package for running poetry projects on emr.',
    'long_description': None,
    'author': 'Richard Brooker',
    'author_email': 'richjbrooker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.9',
}


setup(**setup_kwargs)
