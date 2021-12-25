import pathlib
from setuptools import setup, find_packages


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="fatbeagle-noti",
    version="1.1.0",
    description="Fat Beagle notification system",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Fat-Beagles/fatbeagles-noti",
    author="Fat Beagles",
    author_email="alohanvasu@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
)