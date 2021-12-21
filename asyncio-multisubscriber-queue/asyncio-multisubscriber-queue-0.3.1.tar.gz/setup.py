# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncio_multisubscriber_queue']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pytest = pytest:main']}

setup_kwargs = {
    'name': 'asyncio-multisubscriber-queue',
    'version': '0.3.1',
    'description': 'allow a single producer to provide the same payload to multiple consumers simultaniously',
    'long_description': '#  asyncio-multisubscriber-queue\n\n[![PyPI version](https://img.shields.io/pypi/v/asyncio-multisubscriber-queue)](https://pypi.org/project/asyncio-multisubscriber-queue/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/asyncio-multisubscriber-queue)](https://pypi.org/project/asyncio-multisubscriber-queue/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![](https://github.com/smithk86/asyncio-multisubscriber-queue/workflows/pytest/badge.svg)](https://github.com/smithk86/asyncio-multisubscriber-queue/actions?query=workflow%3Apytest)\n\n## Usage\n\nMultisubscriberQueue allows a single producer to provide the same payload to multiple consumers simultaniously. An asyncio.Queue is created for each consumer and each call to MultisubscriberQueue.put() iterates over each asyncio.Queue and puts the payload on each queue.\n\nPlease see [example.py](https://github.com/smithk86/asyncio-multisubscriber-queue/blob/master/example.py) for a simple example.\n\n## Change Log\n\n### [0.3.1] - 2021-12-21\n\n- Change build system from setuptools to poetry\n\n### [0.3.0] - 2021-11-08\n\n- Add type hints and type validation with mypy\n- Replace _QueueContext object with @contextmanager on MultisubscriberQueue.queue()\n',
    'author': 'Kyle Smith',
    'author_email': 'smithk86@smc3.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/smithk86/asyncio-multisubscriber-queue',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
