# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyprojectx', 'pyprojectx.initializer', 'pyprojectx.wrapper']

package_data = \
{'': ['*']}

install_requires = \
['tomli>=1.2.2,<2.0.0', 'virtualenv>=20.10.0,<21.0.0']

entry_points = \
{'console_scripts': ['pyprojectx = pyprojectx.cli:main']}

setup_kwargs = {
    'name': 'pyprojectx',
    'version': '0.8.3',
    'description': 'Execute scripts from pyproject.toml, installing tools on-the-fly',
    'long_description': '# pyprojectx\n\nExecute scripts from pyproject.toml, installing tools on-the-fly\n\nGetting started with a Python project should be a one-liner:\n```shell\ngit clone https://github.com/houbie/pyprojectx.git && cd pyprojectx && ./pw build\n```\n\n![Cast](https://raw.githubusercontent.com/houbie/pyprojectx/main/docs/poetry-build-cast.svg)\n\nPyprojectx provides a CLI wrapper for automatic installation of Python tools:\n* Make it be a breeze for others to get started with your project or tutorial\n* Get reproducible builds by always using the correct versions of your build tools\n* Plays well with build tools like [Poetry](https://python-poetry.org/) and [PDM](https://pdm.fming.dev/)\n\nPyprojectx brings `npm run` to Python with:\n* less keystrokes\n* isolated dependencies: tools are not required to be development dependencies\n\n## Installation\nCopy the [wrapper scripts](https://github.com/houbie/pyprojectx/releases/latest/download/wrappers.zip)\ninto the root of your project.\n\nPython >= 3.7 must be available on your PATH.\n\n* osx / linux :\n```shell\ncurl -LO https://github.com/houbie/pyprojectx/releases/latest/download/wrappers.zip && unzip wrappers.zip && rm -f wrappers.zip\n```\n\n* windows: unpack the [wrappers zip](https://github.com/houbie/pyprojectx/releases/latest/download/wrappers.zip)\n\n**NOTE** On windows you need to explicitly mark the osx/linux script as executable before adding it to version control.\nWhen using git:\n```shell\ngit add pw pw.bat\ngit update-index --chmod=+x pw\n```\n\n## Configuration\nAdd the _tool.pyprojectx_ section inside _pyproject.toml_ in your project\'s root directory.\n\nEach entry has the form\n\n`tool = "pip-install-arguments"`\n\nExample:\n```toml\n[tool.pyprojectx]\n# require a specific poetry version\npoetry = "poetry==1.1.11"\n# use the latest black\nblack = "black"\n# install flake8 in combination with plugins\nflake8 = """\nflake8\nflake8-bandit\npep8-naming\nflake8-isort\nflake8-pytest-style"""\n```\n\nThe _tool.pyprojectx.aliases_ section can contain optional commandline aliases in the form\n\n`alias = [@tool_key:] command`\n\n\nExample:\n```toml\n[tool.pyprojectx.alias]\n# convenience shortcuts\nrun = "poetry run"\ntest = "poetry run pytest"\npylint = "poetry run pylint"\n\n# tell pw that the bandit binary is installed as part of flake8\nbandit = "@flake8: bandit my_package tests -r"\n\n# simple shell commands (watch out for variable substitutions and string literals containing whitespace or special characters )\nclean = "rm -f .coverage && rm -rf .pytest_cache"\n\n# when running an alias from within another alias, prefix it with `pw@`\ncheck = "pw@pylint && pw@test"\n```\n\nAliases can be invoked as is or with extra arguments:\n```shell\n./pw bandit\n\n./pw poetry run my-script\n# same as above, but using the run alias\n./pw run my-script\n```\n\n## Isolation\nEach tool gets installed in an isolated virtual environment.\n\nThese are all located in in the _.pyprojectx_ directory of your project\n(where _pyproject.toml_ is located).\n\n# Usage\nInstead of calling the commandline of a tool directly, prefix it with `path\\to\\pw`.\n\nExamples:\n```shell\n./pw poetry add -D pytest\ncd src\n../pw black *.py\n```\n\n... or on Windows:\n```shell\npw poetry add -D pytest\ncd src\n..\\pw black *.py\n```\n\nCheck _pw_ specific options with `pw --help`\n\n## Bonus\nIf you want to avoid typing `./pw` (or `../pw` when in a subdirectory), you can install the _px_\nscript in your home directory with `./pw --init global` (or `pw --init global` on Windows) and\nadd _~/.pyprojectx_ to your PATH.\n\nFrom then on, you can replace _pw_ with _px_ and invoke it from any (sub)directory containing the _pw_ script.\n```shell\ncd my-pyprojectx-project\npx test\ncd tests\npx test sometest.py\n```\n\n## Uninstall / cleaning up\n* Delete the _.pyprojectx_ directory in your project\'s root.\n* Delete the global _.pyprojectx_ directory in your home directory.\n\n## Why yet another tool when we already have pipx etc.?\n* As Python noob I had hard times setting up a project and building existing projects\n* There is always someone in the team having issues with his setup, either with a specific tool, with Homebrew, pipx, ...\n* Adding tools as dev dependencies often leads to dependency conflicts\n* Different projects often require different versions of the same tool\n\n## Best practices\n* Separate your tools from your project dependencies\n* Use a build tool with decent dependency management that locks all dependencies,\n  f.e. [Poetry](https://python-poetry.org/) or [PDM](https://pdm.fming.dev/)\n* Pin down the version of your build tool to prevent the "project doesn\'t build anymore" syndrome.\n  Eventually a new version of the build tool with breaking changes will be released.\n* There is a category of tools that you don\'t want to version: tools that interact with changing environments.\n  You probably want to update those on a regular basis by running `./pw --upgrade my-evolving-tool`.\n\n## Examples\n* This project (using Poetry)\n* Projects that still use the **python-wraptor** scripts and need to be migrated to **pyprojectx**\n  * [Pyprojectx examples](https://github.com/houbie/wrapped-pi)\n  * [Facebook\'s PathPicker fork](https://github.com/houbie/PathPicker) (using Poetry)\n\n## Development\n* Build/test:\n```shell\ngit clone git@github.com:houbie/pyprojectx.git\ncd pyprojectx\n./pw build\n```\n\n* Set the path to pyprojectx in the _PYPROJECTX_PACKAGE_ environment variable\n to use your local pyprojectx copy in another project.\n```shell\n# *nix\nexport PYPROJECTX_PACKAGE=path/to/pyprojectx\n# windows\nset PYPROJECTX_PACKAGE=path/to/pyprojectx\n```\n',
    'author': 'Houbie',
    'author_email': 'ivo@houbrechts-it.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/houbie/pyprojectx',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
