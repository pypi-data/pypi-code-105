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
    'version': '0.8.1.1',
    'description': 'A tool that extends configparser to enable enhanced processing of .ini files.',
    'long_description': "<!-- Github Badges -->\n[![ConfigParserEnhanced Testing](https://github.com/sandialabs/ConfigParserEnhanced/actions/workflows/test-driver-core.yml/badge.svg)](https://github.com/sandialabs/ConfigParserEnhanced/actions/workflows/test-driver-core.yml)\n[![Documentation Status](https://readthedocs.org/projects/configparserenhanced/badge/?version=latest)](https://configparserenhanced.readthedocs.io/en/latest/?badge=latest)\n\n\n\nConfigParserEnhanced\n====================\n\nThe ConfigParserEnhanced (CPE) package provides extended\nhandling of .ini files beyond what [ConfigParser][1] provides\nby adding an active syntax to embed operations with options.\n\nFor example, a *standard* `.ini` file is generally formatted like this:\n\n```ini\n[Section 1]\nFoo: Bar\nBaz: Bif\n\n[Section 2]\nFoo: Bar2\nBif: Baz\n```\n\nThese files are used to organize sets of key - value pairs called\n“options” within groups called “sections”. In the example above\nthere are two sections, “Section 1” and “Section 2”. Each of them\ncontains two options where Section 1 has the keys ‘Foo’ and ‘Baz’\nwhich are assigned the values ‘Bar’ and ‘Bif’, respectively. For\nmore details on .ini files please see the documentation for\nConfigParser.\n\nInternally, these handlers methods defined according to a naming\nconvention like `handler_<operation>()`.\n\nCPE only provides one pre-defined operation: use which is formatted as\n`use TARGET:` where *param1* is the TARGET (there is no value field for this\none). The TARGET paramter takes the *name of a target section* that will be\nloaded in at this point. This works in the same way a `#include` would\nwork in C++ and serves to insert the contents or processing of the\ntarget section into this location.\n\nThe `use` operation is useful for .ini files for complex systems by allowing\ndevelopers to create a common section and then have specializations where\nthey can customize options for a given project. For example:\n\n```ini\n[COMMON]\nKey C1: Value C1\nKey C2: Value C2\nKey C3: Value C3\n\n[Data 1]\nKey D1: Value D1\nuse COMMON\nKey D2: Value D2\n```\n\nIn this example, processing section `Data 1` via CPE will result in\nthe following options: `Key D1: Value D1`, `Key C1: Value C1`,\n`Key C2: Value C2`, `Key C2: Value C2`, `Key D2: Value D2`.\n\nAn alternative way of looking at this is it’s like having a .ini file that\nis effectively the following where the `use` operations are replaced with the\nresults of a Depth-First expansion of the linked sections:\n\n```ini\n[COMMON]\nKey C1: Value C1\nKey C2: Value C2\nKey C3: Value C3\n\n[Data 1]\nKey D1: Value D1\nKey C1: Value C1\nKey C2: Value C2\nKey C3: Value C3\nKey D2: Value D2\n```\n\nExamples\n--------\nHere we show some example usages of ConfigParserEnhanced.\nAdditional examples can be found in the [`examples/`](examples) directory\nof the repository.\n\n### Example 1\n\n```ini\n[SECTION-A]\nkey-A1: value-A1\nkey-A2: value-A2\nkey-A3: value-A3\n\n[SECTION-B]\nuse SECTION-A\nkey-B1: value-B1\n```\n\nIn this example, the entry `use SECTION-A` that is inside `[SECTION-B]` instructs the core\nparser to recurse into `[SECTION-A]` and process it before moving on with the rest of the\nentries in `[SECTION-B]`.  In this example the following code could be used to parse\n`SECTION-B`.\n`ConfigParserEnhanced.configparserenhanceddata['SECTION-B']` would return the following\nresult:\n\n```python\n>>> from configparserenhanced import ConfigParserEnhanced\n>>> cpe = ConfigParserEnhanced(filename='config.ini')\n>>> cpe.configparserenhanceddata['SECTION-B']\n{\n    'key-A1': 'value-A1',\n    'key-A2': 'value-A2',\n    'key-A3': 'value-A3',\n    'key-B1': 'value-B1',\n}\n```\n\nUpdates\n=======\nSee the [CHANGELOG][2] for information on changes.\n\n\n[1]: https://docs.python.org/3/library/configparser.html\n[2]: https://github.com/sandialabs/ConfigParserEnhanced/blob/master/CHANGELOG.md\n",
    'author': 'William McLendon',
    'author_email': 'wcmclen@sandia.gov',
    'maintainer': 'Sandia National Laboratories',
    'maintainer_email': 'wg-ConfigParserEnhanced@sandia.gov',
    'url': 'https://github.com/sandialabs/ConfigParserEnhanced',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
