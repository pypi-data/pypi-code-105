# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['links_to_hugo_post']

package_data = \
{'': ['*']}

install_requires = \
['py-executable-checklist>=0.9.0,<0.10.0', 'slug>=2.0,<3.0']

entry_points = \
{'console_scripts': ['links-to-hugo-post = links_to_hugo_post.console:main']}

setup_kwargs = {
    'name': 'links-to-hugo-post',
    'version': '0.3.0',
    'description': 'Convert a list of links to a Hugo blog post',
    'long_description': '# Links to Hugo Post\n\n[![PyPI](https://img.shields.io/pypi/v/links-to-hugo-post?style=flat-square)](https://pypi.python.org/pypi/links-to-hugo-post/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/links-to-hugo-post?style=flat-square)](https://pypi.python.org/pypi/links-to-hugo-post/)\n[![PyPI - License](https://img.shields.io/pypi/l/links-to-hugo-post?style=flat-square)](https://pypi.python.org/pypi/links-to-hugo-post/)\n\n\n---\n\n**Documentation**: [https://namuan.github.io/links-to-hugo-post](https://namuan.github.io/links-to-hugo-post)\n\n**Source Code**: [https://github.com/namuan/links-to-hugo-post](https://github.com/namuan/links-to-hugo-post)\n\n**PyPI**: [https://pypi.org/project/links-to-hugo-post/](https://pypi.org/project/links-to-hugo-post/)\n\n---\n\nConvert a list of links to a Hugo blog post.\n\n## Installation\n\n```sh\npip install links-to-hugo-post\n```\n\n## Example Usage\n\n```shell\n\n```\n\n## Development\n\n* Clone this repository\n* Requirements:\n  * [Poetry](https://python-poetry.org/)\n  * Python 3.7+\n* Create a virtual environment and install the dependencies\n\n```sh\npoetry install\n```\n\n* Activate the virtual environment\n\n```sh\npoetry shell\n```\n\n### Validating build\n\n```sh\nmake build\n```\n\n### Release process\n\nA release is automatically published when a new version is bumped using `make bump`.\nSee `.github/workflows/build.yml` for more details.\nOnce the release is published, `.github/workflows/publish.yml` will automatically publish it to PyPI.\n',
    'author': 'namuan',
    'author_email': 'github@deskriders.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://namuan.github.io/links-to-hugo-post',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
