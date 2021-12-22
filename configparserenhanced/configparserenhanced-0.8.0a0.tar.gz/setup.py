# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['configparserenhanced', 'configparserenhanced.unittests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'configparserenhanced',
    'version': '0.8.0a0',
    'description': 'A tool that extends configparser to enable enhanced processing of .ini files.',
    'long_description': "<!-- Gitlab Badges -->\n<!--\n[![pipeline status](https://gitlab-ex.sandia.gov/trilinos-devops-consolidation/code/ConfigParserEnhanced/badges/master/pipeline.svg)](https://gitlab-ex.sandia.gov/trilinos-devops-consolidation/code/ConfigParserEnhanced/-/commits/master)\n[![coverage report](https://gitlab-ex.sandia.gov/trilinos-devops-consolidation/code/ConfigParserEnhanced/badges/master/coverage.svg)](http://10.202.35.89:8080/ConfigParserEnhanced/coverage/index.html)\n[![Generic badge](https://img.shields.io/badge/docs-latest-green.svg)](http://10.202.35.89:8080/ConfigParserEnhanced/doc/index.html)\n-->\n\n<!-- Github Badges -->\n[![ConfigParserEnhanced Testing](https://github.com/sandialabs/ConfigParserEnhanced/actions/workflows/test-driver-core.yml/badge.svg)](https://github.com/sandialabs/ConfigParserEnhanced/actions/workflows/test-driver-core.yml)\n[![Documentation Status](https://readthedocs.org/projects/configparserenhanced/badge/?version=latest)](https://configparserenhanced.readthedocs.io/en/latest/?badge=latest)\n\n\n\nConfigParserEnhanced\n====================\n\n`ConfigParserEnhanced` (CPE) provides extended functionality for the `ConfigParser` module. This class attempts to satisfy the following goals:\n\n1. Provide a framework to embed extended ‘parsing’ into `Config.ini` style files with customizable\n   _handlers_ that allow 'commands' to be embedded into the key-value structure of typical `.ini`\n   file options.\n2. Enable chaining of `[SECTIONS]` within a single `.ini` file, which uses the parsing capability noted in (1).\n3. Provide an extensible capability. We intend CPE to be used as a base class for other\n   tools so that subclasses can add additional handlers for new ‘operations’ which can be used by the parser.\n\nConfiguration `.ini` File Enhancements\n======================================\nCPE allows `.ini` files to be augmented to embed commands into the `key: value`\nstructure of options within a section.\n\n_Normal_ `.ini` files might have a structure that looks like this:\n\n```ini\n[SECTION NAME]\nkey1: value1\nkey2: value2\nkey4: value3\n```\n\nCPE augments this by allowing the **keys** to be used to embed _operations_.\nTo enable this, CPE attempts to split a key into three pieces, an _operation_, a _parameter_, and\nan optional _uniqueifier_ string.  An option can have an operation extracted as\n`<operation> <parameter> [uniquestr]: value` for example:\n\n```ini\n[SECTION NAME]\noperation1 parameter1: value1\noperation2 parameter2 A: value2\noperation2 parameter2 B: value2\nkey1: value1\nkey2: value2\nkey3: value3\n```\n\n> **Note:** The `[uniquestr]` is optional and we can use it to prevent certain duplicate key errors from the\n> underlying `ConfigParser` which requires that each section must have no duplicate 'key' fields.\n\nWhen the CPE parser successfully identifies a potential _operation_, it will attempt to find a _handler_\nmethod named as `_handler_<operation>()` or `handler_<operation>()`, and if one exists then it will execute\nthat handler with the detected parameter (if any) and value (if any) from that entry.\n\nNew handlers can be added by creating a subclass of CPE and then adding the new handlers to the subclass.\n\nOperations\n==========\nThe CPE base class provides the following handlers by default.\n\n`use`\n----\nThe `use` handler is used in the following manner:\n\n```ini\n[SECTION-A]\nkey-A1: value-A1\nkey-A2: value-A2\nkey-A3: value-A3\n\n[SECTION-B]\nuse SECTION-A\nkey-B1: value-B1\n```\n\nIn this example, the entry `use SECTION-A` that is inside `[SECTION-B]` instructs the core\nparser to recurse into `[SECTION-A]` and process it before moving on with the rest of the\nentries in `[SECTION-B]`.  In this example the following code could be used to parse\n`SECTION-B`.\n`ConfigParserEnhanced.configparserenhanceddata['SECTION-B']` would return the following\nresult:\n\n```python\n>>> cpe = ConfigParserEnhanced(filename='config.ini')\n>>> cpe.configparserenhanceddata['SECTION-B']\n{\n    'key-A1': 'value-A1',\n    'key-A2': 'value-A2',\n    'key-A3': 'value-A3',\n    'key-B1': 'value-B1',\n}\n```\n\nUpdates\n=======\nSee the [CHANGELOG](CHANGELOG.md) for information on changes.\n\nLinks\n=====\nAdditional documentation can be found [here][1].\n\n[1]: http://10.202.35.89:8080/ConfigParserEnhanced/doc/index.html\n",
    'author': 'William McLendon',
    'author_email': 'wcmclen@sandia.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sandialabs/ConfigParserEnhanced',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
