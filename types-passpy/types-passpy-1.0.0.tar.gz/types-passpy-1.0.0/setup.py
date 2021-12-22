from setuptools import setup

name = "types-passpy"
description = "Typing stubs for passpy"
long_description = '''
## Typing stubs for passpy

This is a PEP 561 type stub package for the `passpy` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `passpy`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/passpy. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `40f2cb6e39c4ad7df52f19d8e4f148c55c54a250`.
'''.lstrip()

setup(name=name,
      version="1.0.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['passpy-stubs'],
      package_data={'passpy-stubs': ['__init__.pyi', 'exceptions.pyi', 'store.pyi', 'util.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
