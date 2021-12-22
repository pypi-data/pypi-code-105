# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioinfluxdb']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.8.1,<4.0.0',
 'isal>=0.11.1,<0.12.0',
 'typing-extensions>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'aioinfluxdb',
    'version': '0.1.2',
    'description': 'InfluxDB v2 Python SDK with asyncio support',
    'long_description': '# aioinfluxdb\n\nThe Python client for InfluxDB v2 supports asyncio.\n\n**This is early-stage project**\n\n## Why aioinfluxdb?\n\n[The official client](https://pypi.org/project/influxdb-client/) does not supports asyncio that can get significant\nperformance. and [aioinflux](https://pypi.org/project/aioinflux/) does not supports InfluxDB v2.\n\n## Feature table\n\n| Feature               | Sub category                                                 | ✅ / 🚧 |\n|:----------------------|:-------------------------------------------------------------|:------:|\n| Query                 | Query Data                                                   |   🚧   |\n| Query                 | Analyzer Flux Query                                          |   🚧   |\n| Query                 | Generate AST from Query                                      |   🚧   |\n| Query                 | Retrieve query suggestions                                   |   🚧   |\n| Query                 | Retrieve query suggestions <br /> for a branching suggestion |   🚧   |\n| Write                 |                                                              |   ✅    |\n| Buckets               |                                                              |   🚧   |\n| Dashboards            |                                                              |   🚧   |\n| Tasks                 |                                                              |   🚧   |\n| Resources             |                                                              |   🚧   |\n| Authorizations        |                                                              |   🚧   |\n| Organizations         |                                                              |   🚧   |\n| Users                 |                                                              |   🚧   |\n| Health                |                                                              |   🚧   |\n| Ping                  |                                                              |   ✅    |\n| Ready                 |                                                              |   🚧   |\n| Routes                |                                                              |   🚧   |\n| Backup                |                                                              |   🚧   |\n| Cells                 |                                                              |   🚧   |\n| Checks                |                                                              |   🚧   |\n| DBRPs                 |                                                              |   🚧   |\n| Delete                |                                                              |   🚧   |\n| Labels                |                                                              |   🚧   |\n| NotificationEndpoints |                                                              |   🚧   |\n| NotificationRules     |                                                              |   🚧   |\n| Restore               |                                                              |   🚧   |\n| Rules                 |                                                              |   🚧   |\n| Scraper Targets       |                                                              |   🚧   |\n| Secrets               |                                                              |   🚧   |\n| Setup                 |                                                              |   🚧   |\n| Signin                |                                                              |   🚧   |\n| Signout               |                                                              |   🚧   |\n| Sources               |                                                              |   🚧   |\n| Telegraf Plugins      |                                                              |   🚧   |\n| Telegrafs             |                                                              |   🚧   |\n| Templates             |                                                              |   🚧   |\n| Variables             |                                                              |   🚧   |\n| Views                 |                                                              |   🚧   |',
    'author': 'Byeonghoon Yoo',
    'author_email': 'bh322yoo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
