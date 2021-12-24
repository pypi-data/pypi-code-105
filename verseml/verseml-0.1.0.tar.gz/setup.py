# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['verseml']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['verse = verseml:main']}

setup_kwargs = {
    'name': 'verseml',
    'version': '0.1.0',
    'description': '',
    'long_description': "# Verse ML\n\nA framework for producing production quality ML tools\n\n## Immediate Roadmap\n\n- Build initial API for running training jobs on remote GPUs transparently from the command line.\n- Build initial API for introspecting these jobs while they're running.\n- Build initial API for deploying those models to lambdas/other serverless execution environments.\n",
    'author': 'camjw',
    'author_email': 'camjw119@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/verseml/verseml',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
