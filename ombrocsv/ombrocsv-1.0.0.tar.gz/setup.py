import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ombrocsv",
    version="1.0.0",
    description="Generate random CSV files",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SudoOmbro/csv-gen",
    author="SudoOmbro",
    author_email="ombroso1000@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["csvgen"],
    include_package_data=False,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "ombrocsv=csvgen.__main__:main",
        ]
    },
)