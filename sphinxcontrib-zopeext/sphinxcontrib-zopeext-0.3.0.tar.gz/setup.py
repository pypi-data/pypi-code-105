# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinxcontrib', 'sphinxcontrib.zopeext']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=3.4.2,<5.0.0', 'zope.interface>=5.2.0,<6.0.0']

extras_require = \
{'docs': ['sphinx-book-theme>=0.1.7,<0.2.0']}

setup_kwargs = {
    'name': 'sphinxcontrib-zopeext',
    'version': '0.3.0',
    'description': 'Provides sphinxcontrib.zopeext.autointerface for documenting Zope interfaces.',
    'long_description': '.. -*- rst -*- -*- restructuredtext -*-\n.. Note: this file is simplified without text roles so it displays on PyPI. See\n.. doc/README.rst for the correct information.\n   \n==================\nzopeext for Sphinx\n==================\n\n:author: Michael McNeil Forbes <mforbes@alum.mit.edu>\n\nThis extension provides an `autointerface` directive for `Zope interfaces`_.\n\nRequirements\n============\n\n* Sphinx_: ``pip install sphinx``\n* zope.interface_: ``pip install zope.interface``\n* sphinxcontrib.zopeext_: ``pip install sphinxcontrib-zopeext``\n\nUsage\n=====\n\nIn the `build configuration file`_ (the ``conf.py`` in your Sphinx_\ndocumentation directory) add `sphinxcontrib.zopeext.autointerface` to your\n``extensions`` list::\n\n   extensions = [..., \'sphinxcontrib.zopeext.autointerface\', ...]\n\n\nThen, in your documentation, use `autointerface` as you would use\n`autoclass`.  You can refer to the interface with the ``:py:interface:`` role\n`example.IMyInterface` as you would use the ``:py:class:`` role to refer\nto the implementation `example.MyImplementation`:\n\n.. code-block:: ReST\n\n    .. automodule:: example\n       :show-inheritance:\n       :inherited-members:\n     \nOne can also limit which members are displayed, just as you would with ``.. autoclass``:\n\n.. code-block:: ReST\n\n    .. autointerface:: example.IMyInterface\n       :members: x, equals\n    .. autoclass:: example.MyImplementation\n       :members: x, equals\n\n.. _Sphinx: http://sphinx.pocoo.org/\n.. _build configuration file: http://sphinx.pocoo.org/config.html\n.. _Zope interfaces: http://docs.zope.org/zope.interface/README.html\n.. _zope.interface: http://pypi.python.org/pypi/zope.interface/\n.. _sphinxcontrib.zopeext: http://pypi.python.org/pypi/sphinxcontrib-zopeext/\n\n\n..\n   """\n   Documentation: http://packages.python.org/sphinxcontrib-zopeext\n\n   Install with ``pip install sphinxcontrib-zopeext``.\n\n   To use this extension, include `\'sphinxcontrib.zopeext.autointerface\'` in your\n   `extensions` list in the `conf.py` file for your documentation.\n\n   This provides some support for Zope interfaces by providing an `autointerface`\n   directive that acts like `autoclass` except uses the Zope interface methods for\n   attribute and method lookup (the interface mechanism hides the attributes and\n   method so the usual `autoclass` directive fails.)  Interfaces are intended\n   to be very different beasts than regular python classes, and as a result\n   require customized access to documentation, signatures etc.\n\n   tests_require = [\n       \'Sphinx>=3.3.0\',\n       \'sphinx-testing\',\n       \'pytest>=2.8.1\',\n       \'pytest-cov>=2.2.0\',\n       \'pytest-flake8\',\n       \'coverage\',\n       \'flake8\',\n       \'pep8\',\n\n   """\n',
    'author': 'Michael McNeil Forbes',
    'author_email': 'mforbes@alum.mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
