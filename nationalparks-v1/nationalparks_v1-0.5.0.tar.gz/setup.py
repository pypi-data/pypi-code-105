# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nationalparks_v1', 'nationalparks_v1.data']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.3,<4.0.0',
 'geopy>=2.2.0,<3.0.0',
 'importlib-resources>=5.4.0,<6.0.0',
 'importlib>=1.0.4,<2.0.0',
 'lxml>=4.7.1,<5.0.0',
 'pandas>=1.3.5,<2.0.0',
 'regex>=2021.11.10,<2022.0.0',
 'requests>=2.26.0,<3.0.0',
 'setuptools>=59.6.0,<60.0.0']

setup_kwargs = {
    'name': 'nationalparks-v1',
    'version': '0.5.0',
    'description': 'An API package using US National Park Services API to gather data about US National Parks, such as which parks to go for certain activities, how far a park from a location or the latest alerts in that park. May require user to obatin a free API key from US National Parks website.',
    'long_description': 'Author: Bengusu Ozcan\n# nationalparks_v1\n\nAn API package using US National Park Services API to gather data about US National Parks, such as which parks to go for certain activities, how far a park from a location or the latest alerts in that park. May require user to obatin a free API key from US National Parks website.\n\nSome functions and testing will depend on US National Parks API key. You may obtain one for free via https://www.nps.gov/subjects/developer/get-started.htm\n\n## Testing\n\n## Data\n\n## Installation\n\n```bash\n$ pip install nationalparks_v1\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`nationalparks_v1` was created by Bengusu Ozcan. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`nationalparks_v1` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Bengusu Ozcan',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bengusuozcan/nationalparks_v1',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
