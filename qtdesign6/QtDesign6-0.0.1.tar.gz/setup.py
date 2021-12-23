import codecs
import os.path
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="QtDesign6",
    version=get_version("src\\QtDesign6\\__init__.py"),
    author="Jevex",
    author_email="jevex.endo@gmail.com",
    description="Custom widgets and utilities for PySide6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JevexEndo/qtdesign6",
    project_urls={
        "Bug Tracker": "https://github.com/JevexEndo/qtdesign6/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta ",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
