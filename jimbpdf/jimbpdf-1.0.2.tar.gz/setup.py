import setuptools
from pathlib import Path

pkg = setuptools.find_packages(exclude=["tests", "data"])

setuptools.setup(
    name="jimbpdf",
    version="1.0.2",
    long_description=Path("README.md").read_text(),
    packages=pkg,
)
