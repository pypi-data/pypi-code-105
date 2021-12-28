# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vurf', 'vurf.parser']

package_data = \
{'': ['*'], 'vurf': ['defaults/*']}

install_requires = \
['click>=8.0.0,<9.0.0', 'tomli>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['vurf = vurf.cli:main']}

setup_kwargs = {
    'name': 'vurf',
    'version': '0.11.0',
    'description': "Viliam's Universal Requirements Format",
    'long_description': '# VURF\n![forthebadge](https://forthebadge.com/images/badges/powered-by-black-magic.svg)\n\n![forthebadge](https://forthebadge.com/images/badges/pretty-risque.svg)\n\n![forthebadge](https://forthebadge.com/images/badges/works-on-my-machine.svg)\n\n[![PyPI version](https://badge.fury.io/py/vurf.svg)](https://badge.fury.io/py/vurf)\n\n> Viliam\'s Universal Requirements Format\n\n## What it is\n*VURF* is a format, parser, CLI, and python module for saving packages into Python-ish looking file.\n\n### Example packages.vurf\n```python\nwith pip:\n  vurf\n  black\n  if at_work:\n    ql-cq\n    ql-orange\nwith brew:\n  nnn  # terminal file manager\n```\n\n## Installation\n```sh\npip install vurf\n```\n\n## Usage\n!TODO\n\n## Grammar\n*VURF* has [grammar](./vurf/grammar.lark) and LALR(1) parser implemented in [Lark](https://github.com/lark-parser/lark).\nIt aims to look like Python code as much as possible.\n\n### Keywords\n* `with [section]` - specifies "section" of requirements file. Different sections usually have different installers.\n* `if [condition]:` - conditions for including packages. See [Conditions](##Conditions) sections.\n* `elif [condition]:`\n* `else:`\n* `...` - ellipsis - placeholder for empty section.\n\n### Packages\n* are saved as `[name]  # [comment]`\n* `name` can be almost any valid package name (cannot start with "." or contain tabs or newline characters)\n* names containing spaces must be quoted. E.g. `\'multi word package name\'`\n* comments are optional\n\n## Config\n\nNote: *VURF* will automatically create config file on the first run.\n\n### Config file format\n```toml\n# Where packages file is saved\npackages_location = "/Users/viliam/packages.vurf"\n# Name of the default section\ndefault_section = "brew"\n\n# Sections can be though of as installers for different packages\n# Value of the section is the command for installing packages with `vurf install`\n[sections]\nbrew = "brew install"\ncask = "brew install --cask"\npython = "pip install --quiet --user"\n\n# Parameters are constants that can be accessed from conditionals\n[parameters]\nhostname = "mac"\nprimary_computer = true\nfs = "apfs"\n```\n\n## CLI\n```\n$ vurf\nUsage: vurf [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -q, --quiet  Don\'t produce unnecessary output.\n  --version    Show the version and exit.\n  --help       Show this message and exit.\n\nCommands:\n  add       Add package(s).\n  config    Edit config file.\n  default   Print default section.\n  edit      Edit packages file.\n  format    Format packages file.\n  has       Exit with indication if package is in packages.\n  install   Install packages.\n  packages  Print list of packages.\n  print     Print contents of packages file.\n  remove    Remove package(s).\n  sections  Print list of sections.\n```\n\n## Conditions\n!TODO\n\n## Module\n*VURF* provides python module that exposes approximately the same API as the CLI.\n\n### Example\n```python\nfrom vurf import Vurf\n\npackages = Vurf()\nsections = packages.sections()\npackages.add(\'some-package\', section = sections[1])\nassert packages.has_any(\'some-package\')\npackages.remove([\'other-package\', \'third-package\'])\npackages.save()\n```\n\n## Hooks\n!TODO\n',
    'author': 'Viliam Valent',
    'author_email': 'vurf@valent.email',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ViliamV/vurf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
