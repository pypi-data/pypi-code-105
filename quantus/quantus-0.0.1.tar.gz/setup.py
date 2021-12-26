import setuptools
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quantus",
    version="0.0.1",
    description="A metrics toolkit to evaluate neural network explanations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/understandable-machine-intelligence-lab/Quantus",
    author="Anna Hedström; Franz Motzkus",
    author_email="hedstroem.anna@gmail.com",
    license="MIT",
    packages=["quantus"],
    zip_safe=False,
    python_requires=">=3.6",
)
