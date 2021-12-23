from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A simple utility to get METAR information from the NWSs website. Uses bs4'

# Setting up
setup(
    name="easyweather",
    version=VERSION,
    author="ThomasV2",
    author_email="",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['bs4', 'urllib.request.urlopen'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
