import setuptools
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),'src/'))
from TrimPy import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TrimPy",
    version=__version__,
    author="Ethan Dye",
    author_email="mrtops03@gmail.com",
    description="A tool for interfacing with Trimlight Select systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ecdye/TrimPy",
    project_urls={
        "Bug Tracker": "https://github.com/ecdye/TrimPy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=['TrimPy', 'TrimPy.enum'],
    python_requires=">=3.6",
)
