from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Create cool games just like in unity in python with pygame.'

# Setting up
setup(
    name="myPygameWorkflow",
    version=VERSION,
    author="DuskyElf (Rehmatpal)",
    author_email="<clayedison75@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pygame'],
    keywords=['python', 'pygame', 'gamedev', 'unity', 'scene management'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)