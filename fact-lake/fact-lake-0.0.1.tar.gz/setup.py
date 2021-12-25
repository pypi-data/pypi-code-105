# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fact_lake']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['sphinx<4',
          'sphinx-click>=2.7.1,<3.0.0',
          'sphinx-rtd-theme>=0.5.2,<0.6.0',
          'sphinx-autodoc-typehints>=1.12.0,<2.0.0']}

setup_kwargs = {
    'name': 'fact-lake',
    'version': '0.0.1',
    'description': 'A datalake that is keeping up to date with your factcast',
    'long_description': '# Fact Lake\n\nJust a project stub for now\n\nContributions are welcome. Just get in touch.\n\n## Quickstart\n\nSimply `pip install fact-lake` and get going.\n\n## Development\n\nThis project uses `poetry` for dependency management and `pre-commit` for local checks.\n',
    'author': 'Eduard Thamm',
    'author_email': 'eduard.thamm@thammit.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/edthamm/fact-lake',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
