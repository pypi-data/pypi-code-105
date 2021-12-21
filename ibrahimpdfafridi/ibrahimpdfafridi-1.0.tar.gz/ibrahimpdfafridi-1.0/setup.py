import setuptools
from pathlib import Path
setuptools.setup(
    name = "ibrahimpdfafridi",
    version = 1.0,
    long_description = Path("README.rst").read_text(),
    packages = setuptools.find_packages(),
)