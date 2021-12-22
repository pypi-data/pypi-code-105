# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['deps_helper']
setup_kwargs = {
    'name': 'deps-helper',
    'version': '0.1.3',
    'description': 'dependencies helper',
    'long_description': '# dependency helper\nDependency helper for properties of python class\n\n```python\nfrom deps_helper import Dependencies\n\n\nnew_Dep = Dependencies.new("A")\n\nclass A(new_Dep):\n    #  "_for" can be an array\n    @new_Dep.register(_for="first_operation")[int]  # support type hinting, tested in pyright\n    def number(self, value):\n        return value\n\n    @new_Dep.guard()\n    def first_operation(self):\n        ...\n\n\n>>> a = A()\n>>> a.first_operation()\nTraceback (most recent call last):\n...\nAttributeError: ("follow attributes are not assigned for first_operation => ", [number])\n>>> a.number = 2\n>>> a.first_operation()  # OK\n>>>\n```\n',
    'author': 'jasonyun',
    'author_email': 'killa30865@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ja-sonYun/deps_helper',
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
