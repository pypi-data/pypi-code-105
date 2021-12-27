# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cdn_test']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['cdn-test = cdn_test.cli:entrypoint']}

setup_kwargs = {
    'name': 'cdn-test',
    'version': '0.1.6',
    'description': 'CLI tool to test CDN',
    'long_description': '.. image:: https://badge.fury.io/py/cdn-test.svg\n    :target: https://badge.fury.io/py/cdn-test\n\n.. image:: https://travis-ci.com/augustoliks/cdn-test.svg?branch=main\n    :target: https://travis-ci.com/github/augustoliks/cdn-test\n\ncdn-test\n========\n\nCLI tool created to automate tests for verify time cache in web-site delivered by CDN - CloudFront.\n\nHow to Install\n--------------\n\nThe ``cdn-test`` package is hosted in Python Package Index (PyPI). To\ninstall ``cnd-test``, it\'s recommend create a ``virtualenv`` and install the package using ``pip``. Example:\n\n.. code-block:: bash\n\n    $ virtualenv --python=$(which python3) venv\n    $ source venv/bin/activate\n    $ pip3 install cdn-test\n\nManual\n------\n\n.. code-block:: bash\n\n    $ cdn-test -h\n\n    usage: cli.py [-h] [--url URL] [--time-step [TIME_STEP]] [--http-verb [HTTP_VERB]] [--header-name [HEADER_NAME]] [--output-file [OUTPUT_FILE]] [--version]\n\n    options:\n      -h, --help            show this help message and exit\n      --url URL, -u URL     URL to verified cache in cloudfront\n      --time-step [TIME_STEP], -s [TIME_STEP]\n                            time interval between requests\n      --http-verb [HTTP_VERB], -x [HTTP_VERB]\n                            HTTP verb utilized for requests to URL\n      --header-name [HEADER_NAME]\n                            response header name that contains "Miss from cloudfront" or "Hit from cloudfront"\n      --output-file [OUTPUT_FILE], -f [OUTPUT_FILE]\n                            file path to save records\n      --version, -v         show cdn-test version\n\nExamples\n--------\n\nEach 10 seconds, it will be made a request with ``GET`` HTTP verb to web-site hosted by cloudformation with follow URL ``https://aws.amazon.com/pt/cloudfront/``. The request history will be save on ``~/cdn-report.json``.\n\n.. code-block:: bash\n\n    $ cdn-test --url=https://aws.amazon.com/pt/cloudfront/ --http-verb=GET --time-step=10s --output-file=~/cdn-report.json\n\nPackage Struct\n--------------\n\n.. code-block:: bash\n\n    ├── src\n    │   ├── cdn_test            # source code directory\n    │   ├── __init__.py         # module definition file\n    │   ├── cli.py              # parser cli parameters\n    │   └── domain.py           # module composed only domain logics\n    ├── poetry.lock             # poetry dependencies versions\n    ├── pyproject.toml          # poetry package definition file\n    ├── README.rst              # project documentation\n    └── tests                   # directory composed only with unit tests\n        └── ...\n',
    'author': 'Carlos Neto',
    'author_email': 'carlos.neto.dev@gmail.com',
    'maintainer': 'Carlos Neto',
    'maintainer_email': 'carlos.neto.dev@gmail.com',
    'url': 'https://github.com/augustoliks/cdn-test',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
