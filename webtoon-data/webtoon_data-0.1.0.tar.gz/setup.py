# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['webtoon_data']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'webtoon-data',
    'version': '0.1.0',
    'description': 'Python wrapper for Webtoon data',
    'long_description': "# webtoon_data\n\nA preliminary attempt at a Python API wrapper for Webtoon data. For obtaining lists of Webtoon titles and rankings.\n\n## Installation\n\n```bash\n$ pip install webtoon_data\n```\n\n## Usage\n\nProvide genre list available in WEBTOON.\n\n```\n>>> get_webtoon_genre_list\n>>> ['Drama', 'Fantasy', 'Comedy', 'Action', 'Slice of life', 'Romance', 'Superhero', 'Sci-fi', 'Thriller', 'Supernatural', 'Mystery', 'Sports', 'Historical', 'Heart-warming', 'Horror', 'Informative']\n```\n\nWhat are the top ranking WEBTOON in specified genre?\n\n```\n>>> get_webtoon_list_ranking('ROMANCE')\n>>> [1320, 1218, 1798, 1436, 1468, 2606, 2832, 218...\n```\n\n## License\n\n`webtoon_data` was created by Kim Eunji. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`webtoon_data` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n",
    'author': 'Kim Eunji',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
