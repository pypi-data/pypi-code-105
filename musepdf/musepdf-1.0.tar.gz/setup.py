import setuptools
from pathlib import Path

setuptools.setup(
    name="musepdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
# setup file
# python setup.py sdist bdist_wheel
# sdist for source distribution, bdist for build distribution
# this command will generate two distr packages

# twine upload dist/* --> upload into pipy
