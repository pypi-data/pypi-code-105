# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['l9format']

package_data = \
{'': ['*']}

install_requires = \
['serde>=0.8.1,<0.9.0']

setup_kwargs = {
    'name': 'l9format',
    'version': '1.3.1.post0',
    'description': 'l9format is a schema declaration targeted at interoperability between network recon tools used at LeakIX',
    'long_description': 'l9format python\n===================\n\nl9format is a schema declaration targeted at interoperability between network\nrecon tools used at LeakIX.\n\nThis library is equivalent to [l9format](https://github.com/leakix/l9format)\nwhich provides a Go implementation.\n\n## Run the tests\n\n\n```\npoetry install\npoetry run pytest l9format/tests/test_l9format.py\n```\n\n## Install\n\nUse main branch for the moment:\n```\npoetry add https://github.com/leakix/l9format-python#main\n```\n\n## Documentation\n\n```\nfrom l9format import l9format\nl9format.L9Event.from_dict(res)\n```\n\n## Versioning\n\nThe versions will be synced with [l9format](https://github.com/leakix/l9format),\nsuffixed by a number for bug fixes in the python implementation specifically.\nFor instance, `1.3.1-0` will be the first version for `1.3.1` and follow\nhttps://github.com/LeakIX/l9format/releases/tag/v1.3.1. If a change is required\nfor the Python package, but is the same specification than the Go\nimplementation, the next release will be `1.3.1-1`.\n',
    'author': 'Danny Willems',
    'author_email': 'danny@leakix.net',
    'maintainer': 'Danny Willems',
    'maintainer_email': 'danny@leakix.net',
    'url': 'https://github.com/leakix/l9format-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
