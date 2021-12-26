# python setup.py sdist bdist_wheel
# twine upload dist/*
from setuptools import setup

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='planetoidAI',                           # should match the package folder
    packages=['planetoidAI'],                     # should match the package folder
    version='0.0.1',                                # important for updates
    license='MIT',                                  # should match your chosen license
    description="Planetoid's official library to access free API",
    long_description=long_description,              # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Himanshu Moliya (Founder)',
    url='https://github.com/HimanshuMoliya/planetoid.git', 
    project_urls = {                                # Optional
        "Bug Tracker": "https://github.com/HimanshuMoliya/planetoid/issues"
    },
    install_requires=['requests'],                  # list all packages that your package uses
    keywords=["pypi", "planetoid", "planetoid-api", "free", "api","himanshumoliya", "himanshu"], #descriptive meta-data
    lassifiers=[                                   # https://pypi.org/classifiers
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],    
    download_url="https://pypi.org/project/planetoid_api/0.0.1/",
)