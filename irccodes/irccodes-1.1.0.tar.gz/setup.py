from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='irccodes',
    version='1.1.0',
    author='Tomas Globis',
    description='',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type="text/markdown",
    url='https://github.com/TomasGlgg/irccodes',
    classifiers=[
            "Programming Language :: Python :: 3",
    ]
)
