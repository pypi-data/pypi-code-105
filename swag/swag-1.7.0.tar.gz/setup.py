# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['swag']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['swag = swag.__main__:main']}

setup_kwargs = {
    'name': 'swag',
    'version': '1.7.0',
    'description': 'Swag up your shell output with escape code magic!',
    'long_description': '# Swag\n\nColor your shell output with escape code magic.\n\n![Demo](https://media.giphy.com/media/l0O5ASEoXnoaMd3S8/source.gif)\n\n## Installation\n\n`pip install swag`\n\n## Usage\n\n\n```\nusage: swag [-h] {print,install} ...\n\npositional arguments:\n  {print,install}  [command] help\n    install        install the colors to the folder of choice\n    print          prints the text with the specified color and type to the\n                   console\n\noptional arguments:\n  -h, --help       show this help message and exit\n```\n\n## Raw Usage\n\n\n\n### Use from code\n\n```\nfrom swag import colors\nprint colors.COLORS["red"], "This will be red"\n\n# Or use the swagprinter helpers:\n\n\nfrom swag import swagprinter\nfrom swag.swagprinter import INTENSE\n\nswagprinter.print_green("Blah", INTENSE) # Prints an intense green\n\n# Prints an intense green, to the end of the output:\nswagprinter.print_green("Blah", INTENSE, true)\n\n```\n\n### Installation to a folder\n\nFrom the commandline do\n\n```\nswag install -d <path/to/folder> # default is ~/.colors\n```\n\nThis will install all the escape codes to the ~/.colors or <path/to/folder> folder.\n\nNow you can use the colors directly from the console via:\n\n`echo $(cat ~/.colors/blue) This will be blue`\n',
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
