# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['portchecker']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['portcheck = portchecker.port_checker:main']}

setup_kwargs = {
    'name': 'portcheckerio',
    'version': '0.1.3',
    'description': 'A new way to query the ports of a given hostname of IP address',
    'long_description': '<h1 align="center">Welcome to portcheckerio 👋</h1>\n\n![PyPI](https://img.shields.io/pypi/v/portcheckerio)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/portcheckerio)\n[![GitHub license](https://img.shields.io/github/license/dsgnr/portchecker)](https://github.com/dsgnr/portchecker/blob/devel/LICENSE)\n[![Pytest](https://github.com/dsgnr/portchecker/actions/workflows/pytest.yml/badge.svg)](https://github.com/dsgnr/portchecker/actions/workflows/pytest.yml)\n[![CodeQL](https://github.com/dsgnr/portchecker/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/dsgnr/portchecker/actions/workflows/codeql-analysis.yml)\n\nThis repository is the counterpart script which ports [portchecker.io](https://portchecker.io)\n\nThis package is a nice alternative way to using tools like `nc` to query the port connectivity. \nThe main benefits is that it will work with hostnames, \nIPv4 and IPv6 addresses (if your client has IPv6 of course). \nYou can also query multiple ports at the same time and receive a sweet JSON response.\n\n## Installation\n\nPortchecker can be installed from PyPI using `pip` or your package manager of choice:\n\n```\npip install portcheckerio\n```\n\n## Usage\n\n### CLI\n\nYou can use Portchecker as a CLI tool using the `portcheck` command.\n\nExample:\n\n```console\n$ portcheck --host google.com --ports 443\n{\n    "2a00:1450:4009:815::200e": {\n        "type": "ipv6",\n        "results": [\n            {\n                "port": 443,\n                "connectable": true\n            }\n        ]\n    },\n    "172.217.16.238": {\n        "type": "ipv4",\n        "results": [\n            {\n                "port": 443,\n                "connectable": true\n            }\n        ]\n    }\n}\n```\n\nYou can query multiple ports for a given host in the same command:\n\n```console\n$ portcheck --host google.com --ports 443 22\n{\n    "172.217.16.238": {\n        "type": "ipv4",\n        "results": [\n            {\n                "port": 443,\n                "connectable": true\n            },\n            {\n                "port": 22,\n                "connectable": false\n            }\n        ]\n    },\n    "2a00:1450:4009:815::200e": {\n        "type": "ipv6",\n        "results": [\n            {\n                "port": 443,\n                "connectable": true\n            },\n            {\n                "port": 22,\n                "connectable": false\n            }\n        ]\n    }\n}\n```\n\n## 📝 To Do\n\n- [ ] Add more tests \n- [ ] Add the option to query RFC1918 addresses\n- [ ] Add the option to increase the timeout limit \n\n### 🏠 [Homepage](https://portchecker.io)\n\n### ✨ [Demo](https://portchecker.io)\n\n## Author\n\n👤 **Dan Hand**\n\n* Website: https://danielhand.io\n* Github: [@dsgnr](https://github.com/dsgnr)\n\n## 🤝 Contributing\n\nContributions, issues and feature requests are welcome.<br />\nFeel free to check [issues page](https://github.com/dsgnr/portchecker.io/issues) if you want to contribute.<br />\n\n\n## Show your support\n\nGive a ⭐️ if this project helped you!\n\nAny donations to help the running of the site is hugely appreciated!\n\n<a href="https://www.patreon.com/dsgnr_">\n  <img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="100">\n</a>\n<a href="https://www.paypal.com/donate?business=RNT9HTKVJ2DDJ&no_recurring=0&item_name=portchecker.io+donation&currency_code=GBP" target="_blank"><img src="https://www.paypalobjects.com/en_GB/i/btn/btn_donate_SM.gif"></a>\n\n\n## 📝 License\n\nCopyright © 2019 [Dan Hand](https://github.com/dsgnr).<br />\nThis project is [MIT](https://github.com/kefranabg/readme-md-generator/blob/master/LICENSE) licensed.\n\n---\n***\n_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_\n',
    'author': 'Dan Hand',
    'author_email': 'info@portchecker.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dsgnr/portchecker',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>3.6.2,<4.0',
}


setup(**setup_kwargs)
