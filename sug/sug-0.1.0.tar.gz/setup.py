# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sug']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['sug = sug.__main__:app']}

setup_kwargs = {
    'name': 'sug',
    'version': '0.1.0',
    'description': 'A generator for systemd unit files',
    'long_description': '# sug - systemd unit generator\n\n![sug.png](https://raw.githubusercontent.com/4thel00z/logos/master/sug.png)\n\n## Motivation\n\nI am on a fresh server and want to have systemd unit. It has python installed.\n\n## Installation\n\n```sh\npip install sug\n```\n\nBetter:\n\n```sh\npipx install sug\n```\n\n## Usage\n\nSug is pretty simple, you can invoke it like this:\n```\nUsage: sug [OPTIONS] NAME WORKING_DIR EXEC_START BIN_PATH USER GROUP\n```\n\n## Example\n\nThis is an invocation example for sug:\n\n```sh\nsug "myservice" /var/run/myservice "$(which myservice) --verbose" $(which myservice) $USER $USER \n```\n',
    'author': '4thel00z',
    'author_email': '4thel00z@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/4thel00z/sug',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
