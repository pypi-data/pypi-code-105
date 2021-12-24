# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['databooks', 'databooks.data_models']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.24,<4.0.0',
 'mkdocs-coverage>=0.2.4,<0.3.0',
 'pydantic>=1.8.2,<2.0.0',
 'rich>=10.6.0,<11.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['databooks = databooks.cli:app']}

setup_kwargs = {
    'name': 'databooks',
    'version': '0.1.0',
    'description': 'A CLI tool to resolve git conflicts and remove metadata in notebooks.',
    'long_description': '<img align="left" style="padding: 10px" width="120" height="120" src="https://raw.githubusercontent.com/datarootsio/databooks/main/docs/images/logo.png?token=AKUGIEI3HBAW32EUFUD5AT3BXT6BC">\n\n# databooks\n[![maintained by dataroots](https://dataroots.io/maintained-rnd.svg)](https://dataroots.io)\n[![PythonVersion](https://img.shields.io/pypi/pyversions/databooks)](https://img.shields.io/pypi/pyversions/databooks)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)\n[![Codecov](https://codecov.io/github/datarootsio/databooks/badge.svg?branch=main&service=github)](https://github.com/datarootsio/databooks/actions)\n[![tests](https://github.com/datarootsio/databooks/workflows/tests/badge.svg?branch=main)](https://github.com/datarootsio/databooks/actions)\n[![PythonVersion](https://img.shields.io/pypi/l/databooks)](https://img.shields.io/pypi/l/databooks)\n\n\n`databooks` is a package for reducing the friction data scientists while using [Jupyter\nnotebooks](https://jupyter.org/), by reducing the number of git conflicts between\ndifferent notebooks and assisting in the resolution of the conflicts.\n\nThe key features include:\n\n- CLI tool\n  - Clear notebook metadata\n  - Resolve git conflicts\n- Simple to use\n- Simple API for using modelling and comparing notebooks using [Pydantic](https://pydantic-docs.helpmanual.io/)\n\n## Requirements\n\n`databooks` is built on top of:\n- Python 3.8+\n- [Typer](https://typer.tiangolo.com/)\n- [Rich](https://rich.readthedocs.io/en/latest/)\n- [Pydantic](https://pydantic-docs.helpmanual.io/)\n- [GitPython](https://gitpython.readthedocs.io/en/stable/tutorial.html)\n\n## Installation\n\n```\npip install databooks\n```\n\n## Usage\n\n### Clear metadata\n\nSimply specify the paths for notebook files to remove metadata. By doing so, we can \nalready avoid many of the conflicts.\n\n```console\n$ databooks meta [OPTIONS] PATHS...\n```\n\n![databooks meta demo](https://raw.githubusercontent.com/datarootsio/databooks/main/docs/images/databooks-meta.gif?token=AKUGIEOHIY4XVJK2IRRMNRLBYJBEQ)\n\n### Fix git conflicts for notebooks\n\nSpecify the paths for notebook files with conflicts to be fixed. Then, `databooks` finds\nthe source notebooks that caused the conflicts and compares them (so no JSON manipulation!)\n\n```console\n$ databooks fix [OPTIONS] PATHS...\n```\n\n![databooks fix demo](https://raw.githubusercontent.com/datarootsio/databooks/main/docs/images/databooks-fix.gif?token=AKUGIELRRMXJMU7RSUUGYUDBYJD5G)\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Murilo Cunha',
    'author_email': 'murilo@dataroots.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://datarootsio.github.io/databooks/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
