# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['log4j_detector_to_csv']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['log4j-detector-to-csv = log4j_detector_to_csv.main:main']}

setup_kwargs = {
    'name': 'log4j-detector-to-csv',
    'version': '0.1.2',
    'description': 'Combines all host specific json outputs from log4j-detector into one single csv file.',
    'long_description': None,
    'author': 'Richard Bischof',
    'author_email': 'richard.bischof@lgln.niedersachsen.de>, Maik Fischer <maik.fischer@lgln.niedersachsen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/richardbischof/log4j-detector-to-csv',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
