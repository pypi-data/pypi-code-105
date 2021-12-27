# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thcrdt']

package_data = \
{'': ['*']}

install_requires = \
['thquickjs>=0.9.0,<0.10.0', 'thresult>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'thcrdt',
    'version': '0.9.1',
    'description': 'TangledHub Thcrdt Library',
    'long_description': "[![Build][build-image]]()\n[![Stable Version][stable-image]][stable-url]\n[![Coverage][coverage-image]]()\n[![License][bsd3-image]][bsd3-url]\n\n\n# THCRDT\n\n## Overview\n\nTangledHub library that handles Conflict-free Replicated Data types.\n\n## Licencing\nthcrdt is licensed under the BSD license. Check the [LICENSE](https://opensource.org/licenses/BSD-3-Clause) for details.\n\n---\n\n## Installation\n```bash\npip install thcrdt\n```\n\n## Testing\n```bash\ndocker-compose build thcrdt-test ; docker-compose run --rm thcrdt-test\n```\n\n## Building\n```bash\ndocker-compose build thcrdt-builning ; docker-compose run --rm thcrdt-builning\n```\n\n## Publish\n```bash\ndocker-compose build thcrdt-publish ; docker-compose run --rm thcrdt-publish\n```\n\n---\n\n## CRDT supported in this library\n\n### CRDT_Dict\n```python\ndoc: dict = crdt.from_({'cards': [{'x': 0, 'y': 10, 'z': 20}]}).unwrap()\n```\n\n### CRDT_List\n```python\ndoc: dict = crdt.from_({'cards': [[1, 2, 3]]}).unwrap()\n```\n\n### CRDT_Counter\n```python\ndoc: dict = crdt.from_({'cards': [Counter(1)]}).unwrap()\n```\n\n#### increment(int)\nIncrease counter value\n```python\ndoc['cards'][0].increment(2)\n```\n\n#### decrement(int)\nDecrease counter value\n```python\ndoc['cards'][0].decrement(1)\n```\n\n## API\nthcrdt api is using the **thresult** library, so all api functions are returning result wrapped in **Ok** or **Err** object.  \nTherefore, in order to reach into the result object, you should use **.unwrap()** as in examples.\n```python\ncrdt = CRDT()\n```\n\n### crdt.from_(self, o: Any)\nCreates a new CRDT object and populates it with the contents of the passed object\n#### Example:\nCreate document with initial state\n```python\ndoc_s0: dict = crdt.from_({'cards': [{'x': 0}]}).unwrap()\n```\n\n\n### crdt.clone(self, Any)\nCreates a new copy of the CRDT instance\n#### Example:\n```python\ndoc_clone = crdt.clone(doc_s0)\n```\n\n\n### crdt.change(self, doc: Any, fn: Callable)\nModify an CRDT object, returning an updated copy\n#### Example:\n```python\n# CLIENT A\n# changes on client A\ndef doc_ca(doc: dict):\n    doc['cards'][0]['x'] = 5\n    doc['cards'][0]['y'] = 10\n    doc['cards'][0]['z'] = 20\n    \n# The doc_a0 object is treated as immutable, you must never change it directly, create doc_a0 clone using crdt.clone().\n# In order to update doc_a0 you should use crdt.change() instead.\ndoc_a1: dict = crdt.change(crdt.clone(doc_s0).unwrap(), doc_ca).unwrap()\n```\n\n\n### crdt.merge(self, a: Any, b: Any)\n#### Example:\nMerges the two CRDT instances\n```python\n# CLIENT B\n# Create initial document on client B\ndoc_b0: dict = crdt.from_({'cards': [{}]}).unwrap()\n\n# Now merge this two documents\ndoc_b1: dict = crdt.merge(doc_b0, doc_a1).unwrap()\n```\n```python\n# changes on client B\ndef doc_cb(doc: dict):\n    doc['cards'][0]['x'] = -5\n    doc['cards'][0]['y'] = -10\n    doc['cards'][0]['z'] = -20\n```\n```python\ndoc_b2: dict = crdt.change(crdt.clone(doc_s0).unwrap(), doc_cb).unwrap()\n```\n```python\n# Now merge the changes from client B back into client A. You can also\n# do the merge the other way round, and you'll get the same result.\nfinal_doc: dict = crdt.merge(doc_b2, doc_a1).unwrap()\n```\n\n\n### crdt.get_changes(self, root: Any, doc: Any)\nReturns a list of all the changes that were made in the document\n#### Example:\n```python\n# Create document with initial state\ndoc1s: dict = crdt.from_({'cards': [{}]}).unwrap()\n```\n```python\n# CLIENT A\n# changes on client A\ndef doc_ca(doc: dict):\n    doc['cards'][0]['x'] = 5\n    doc['cards'][0]['y'] = 10\n    doc['cards'][0]['z'] = 20\n```\n```python\n# In order to update doc1s you should use crdt.change().\ndoc_a1: dict = crdt.change(crdt.clone(doc1s).unwrap(), doc_ca).unwrap()\n```\n```python\n# Get changes made on client A. These changes are encoded as byte arrays (Uint8Array)\ndoc_a1_changes: list = crdt.get_changes(doc1s, doc_a1).unwrap()\n```\n\n\n### crdt.apply_changes\nApplies the list of changes to the given document, and returns a new document with those changes applied\n#### Example:\n```python\n# CLIENT B\n# Now apply changes on client B\ndoc_b1, patch = crdt.apply_changes(doc1s, doc_a1_changes).unwrap()\n```\n\n\n<!-- Links -->\n\n<!-- Badges -->\n[bsd3-image]: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg\n[bsd3-url]: https://opensource.org/licenses/BSD-3-Clause\n[build-image]: https://img.shields.io/badge/build-success-brightgreen\n[coverage-image]: https://img.shields.io/badge/Coverage-100%25-green\n[stable-image]: https://img.shields.io/pypi/v/thcrdt?label=stable\n[stable-url]: https://pypi.org/project/thcrdt/\n\n",
    'author': 'TangledHub',
    'author_email': 'info@tangledgroup.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/tangledlabs/thcrdt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
