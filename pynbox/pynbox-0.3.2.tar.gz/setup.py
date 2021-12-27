# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pynbox', 'pynbox.entrypoints']

package_data = \
{'': ['*'], 'pynbox': ['assets/*']}

install_requires = \
['click>=8.0.3',
 'goodconf[yaml]>=2.0.1,<3.0.0',
 'questionary>=1.10.0',
 'repository-orm>=0.7.0',
 'rich>=10.16.1']

entry_points = \
{'console_scripts': ['autodev = autodev.entrypoints.cli:cli',
                     'pynbox = pynbox.entrypoints.cli:cli']}

setup_kwargs = {
    'name': 'pynbox',
    'version': '0.3.2',
    'description': 'Task management inbox tool',
    'long_description': '# pynbox\n\n[![Actions Status](https://github.com/lyz-code/pynbox/workflows/Tests/badge.svg)](https://github.com/lyz-code/pynbox/actions)\n[![Actions Status](https://github.com/lyz-code/pynbox/workflows/Build/badge.svg)](https://github.com/lyz-code/pynbox/actions)\n[![Coverage Status](https://coveralls.io/repos/github/lyz-code/pynbox/badge.svg?branch=master)](https://coveralls.io/github/lyz-code/pynbox?branch=master)\n\nTask management inbox tool\n\n## Help\n\nSee [documentation](https://lyz-code.github.io/pynbox) for more details.\n\n## Installing\n\n```bash\npip install pynbox\n```\n\n## Contributing\n\nFor guidance on setting up a development environment, and how to make\na contribution to *pynbox*, see [Contributing to\npynbox](https://lyz-code.github.io/pynbox/contributing).\n\n## License\n\nGPLv3\n',
    'author': 'Lyz',
    'author_email': 'lyz-code-security-advisories@riseup.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lyz-code/pynbox',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<=3.10',
}


setup(**setup_kwargs)
