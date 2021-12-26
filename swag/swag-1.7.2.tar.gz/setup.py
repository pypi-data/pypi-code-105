# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swag']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['swag = swag.__main__:app']}

setup_kwargs = {
    'name': 'swag',
    'version': '1.7.2',
    'description': 'Swag up your shell output with escape code magic!',
    'long_description': '# Swag\n\nColor your shell output with escape code magic.\n\n![Demo](https://media.giphy.com/media/l0O5ASEoXnoaMd3S8/source.gif)\n\n## Installation\n\n`pip install swag`\n\n## Usage\n\n```\nUsage: swag [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n\n  --help                          Show this message and exit.\n\nCommands:\n  install\n  list\n  print\n```\n\n## CLI Usage\n\n### Print to the cli\n\nYou can print colored from the shell as follows:\n\n```shell\nswag print --color yellow --modifier intenseBold "This text will be intenseBold and yellow :-)"\n```\n\nThe possible modifiers are:\n\n* underline\n* background\n* bold\n* intense\n* intenseBold\n* intenseBackground\n\n### Installation to a folder\n\nFrom the commandline do:\n\n```shell\nswag install --dest <path/to/folder> # default is ~/.colors\n```\n\nThis will install all the escape codes to the ~/.colors or <path/to/folder> folder.\n\nNow you can use the colors directly from the console via:\n\n`echo $(cat ~/.colors/blue) This will be blue`\n\n### List all colors\n\nPrints a list of colors (color coded).\n\n```shell\nswag list\n```\n\n## Use from code\n\n```python\nfrom swag import red, green, reset, INTENSE\n\nred("This will be red")\ngreen("Blah", modifier=INTENSE)  # Prints an intense green\n# Prints an intense green, to the end of the output, means if you use print after it will be green too:\ngreen("This is green until the end", modifier=INTENSE, continuous=True)\nprint("This will still be green")\nreset()  # From now on the default cli color will be used\n```\n## License\n\nThis project is licensed under the GPL-3 license.\n',
    'author': '4thel00z',
    'author_email': '4thel00z@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
