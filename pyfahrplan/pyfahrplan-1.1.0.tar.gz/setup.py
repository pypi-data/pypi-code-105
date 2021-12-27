# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfahrplan']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0,<9.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.26.0,<3.0.0',
 'requests_cache>=0.8.1,<0.9.0',
 'rich>=10.16.1,<11.0.0']

entry_points = \
{'console_scripts': ['pyfahrplan = pyfahrplan.pyfahrplan_cli:cli']}

setup_kwargs = {
    'name': 'pyfahrplan',
    'version': '1.1.0',
    'description': 'A CCC Fahrplan CLI',
    'long_description': "# pyfahrplan\n\nCLI application for CCC several fahrplan files (schedule.json), currently based on:\n\n - https://raw.githubusercontent.com/voc/{32-36}C3_schedule/master/everything.schedule.json\n - https://data.c3voc.de/rC3/everything.schedule.json\n - https://data.c3voc.de/rC3_21/everything.schedule.json\n\n## Usage\n\n```\nUsage: pyfahrplan [OPTIONS]\n\nOptions:\n  -c, --conference TEXT           CCC acronym (32c3 to 36c3 plus rc3 and\n                                  rc3-2021) that you want to filter on, 'all'\n                                  for all conferences\n  -d, --day INTEGER               Day you want to filter [1-4] or 0 for all\n                                  days.\n  -r, --room TEXT                 Name of the room you want to filter [room\n                                  names] or 'all' for all rooms\n  -s, --speaker TEXT              Name of a speaker you want to search.\n  -st, --start [%H:%M]            Start time of the talk(s) you want to\n                                  search.\n  -t, --title TEXT                A part of the title of the talk(s) you want\n                                  to search.\n  -tr, --track TEXT               A part of the track description you want to\n                                  search.\n  --reverse                       Reverse results\n  --show-abstract                 Shows abstracts, default False\n  --show-description              Shows descriptions, default False\n  --sort [day|speakers|title|track|room|talk_start]\n                                  Sort by\n                                  day|speakers|title|track|room|talk_start\n  --update-cache                  Delete the cache file and redownload all\n                                  fahrplans\n  --no-past                       Filter out talks that lay in the past\n  --help                          Show this message and exit.\n```\n\n## Development\n\nClone this repository, then create a virtualenv, e.g., inside the repository:\n\n```bash\npython3 -m venv .venv\npip install poetry  # if you don't have it globally installed\npoetry install  # install all dependencies, including dev dependencies\npoe test  # to run the tests\npytest --cov=pyfahrplan tests/ && coverage html  # to create a coverage report\n```\n",
    'author': 'Sascha',
    'author_email': 'saschalalala@github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/saschalalala/pyfahrplan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
