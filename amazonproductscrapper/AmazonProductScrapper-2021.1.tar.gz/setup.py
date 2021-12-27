from setuptools import setup, find_packages
import pathlib

VERSION = '2021.1'
DESCRIPTION = 'AmazonProductScrapper'
#LONG_DESCRIPTION = 'Extract Products and its associated data from a keyword and also extract reviews about a particular product'
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="AmazonProductScrapper",
        version=VERSION,
        author="Subhajit Saha",
        author_email="subhajitsaha.formal@gmail.com",
        description=DESCRIPTION,
        long_description=README,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        install_requires=['pandas','requests','bs4'], # add any additional packages that
        # needs to be installed along with your package. Eg: 'caer'
        url="https://github.com/subhajit2001/AmazonProductScrapper",
        license="MIT",
        keywords=['python', 'Amazon Product Scrapper','Scrapper','Amazon','Product Scrapper'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
