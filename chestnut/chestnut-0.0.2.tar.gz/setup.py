from setuptools import setup, find_packages
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


NAME = "chestnut"
VERSION = "0.0.2"
REQUIRES = [
    "pyfir>=0.0.5"
]


setup(
    name=NAME,
    version=VERSION,
    description="Framework to develop multi cloud APIs.",
    author="Claudjos",
    author_email="claudjosmail@gmail.com",
    url="https://github.com/Claudjos/chestnut",
    keywords=["Web App", "Multi Cloud"],
    install_requires=REQUIRES,
    packages=find_packages(),
    long_description_content_type='text/markdown',
    long_description=long_description
)
