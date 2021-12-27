from setuptools import setup, find_packages

VERSION = '2021.0'
DESCRIPTION = 'AmazonProductScrapper'
LONG_DESCRIPTION = 'Extract Products and its associated data from a keyword'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="AmazonProductScrapper",
        version=VERSION,
        author="Subhajit Saha",
        author_email="<subhajitsaha.formal@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['pandas','requests','bs4'], # add any additional packages that
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'Amazon Product Scrapper','Scrapper','Amazon','Product Scrapper'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
