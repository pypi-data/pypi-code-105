# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nv',
 'nv.utils',
 'nv.utils.collections',
 'nv.utils.collections.mappings',
 'nv.utils.collections.sequences',
 'nv.utils.collections.structures',
 'nv.utils.formatters',
 'nv.utils.introspect',
 'nv.utils.models',
 'nv.utils.parsers',
 'nv.utils.parsers.string',
 'nv.utils.serializers',
 'nv.utils.tables']

package_data = \
{'': ['*']}

extras_require = \
{':extra == "pytz" or extra == "all"': ['pytz>=2021.1,<2022.0'],
 'all': ['openpyxl>=3.0.5,<4.0.0',
         'xlrd>=2.0.1,<3.0.0',
         'xlwt>=1.3.0,<2.0.0',
         'msgpack-python>=0.5.6,<0.6.0',
         'xmltodict>=0.12.0,<0.13.0',
         'dicttoxml>=1.7.4,<2.0.0'],
 'msgpack': ['msgpack-python>=0.5.6,<0.6.0'],
 'xls': ['xlrd>=2.0.1,<3.0.0', 'xlwt>=1.3.0,<2.0.0'],
 'xlsx': ['openpyxl>=3.0.5,<4.0.0'],
 'xml': ['xmltodict>=0.12.0,<0.13.0', 'dicttoxml>=1.7.4,<2.0.0']}

setup_kwargs = {
    'name': 'nv-utils',
    'version': '0.2.0',
    'description': 'Parsers, formatters, data structures and helpers for Python 3 (>=3.9)',
    'long_description': "# nv.utils\nParsers, formatters, data structures and other helpers for Python 3. This is a source of recurring\nportions of reusable code that we needed in our applications, such as tools for configuration parsing,\nvalue casting, data structures, etc.\n\n## What's inside?\n[to come]\n\n\n## Important message on Python for v0.2 and Python < 3.9\nSubstantial changes have been made on the organization of nv-utils for the long run, with breaking changes vs. 0.1.15.\n\n## Disclaimers\nTHIS IS UNDOCUMENTED WORK IN PROGRESS. READ THE LICENSE AND USE IT AT YOUR OWN RISK.\n\nTHIS IS STILL A BETA AND BREAKING CHANGES MAY (AND PROBABLY WILL) OCCUR UNTIL ITS CONTENT STABILIZES. WE\nARE ACTIVELY MIGRATING STUFF OUT OF THIS LIBRARY (AND LOOKING FOR SUBSTITUTES THAT ARE MORE ACTIVELY MAINTAINED)\n",
    'author': 'Gustavo Santos',
    'author_email': 'gustavo@next.ventures',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gstos/nv-utils',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
