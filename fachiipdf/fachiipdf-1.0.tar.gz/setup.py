import setuptools
from pathlib import Path

setuptools.setup(
    name="fachiipdf",
    version=1.0,
    description=Path("/home/fachiis/Desktop/codes/fachiispdf/README.md").read_text(),
    packages=setuptools.find_packages(exclude=["data", "tests"]),
)
