import os

from setuptools import setup, find_packages

setup(
    name="glapi",
    description="Python package to interact with GitLab API.",
    long_description=open(os.path.join(os.getcwd(), "README.md")).read().strip(),
    version=open(os.path.join(os.getcwd(), "VERSION")).read().strip(),
    url="https://gitlab.com/lgensinger/mkdpdf",
    install_requires=[d.strip() for d in open(os.path.join(os.getcwd(), "requirements.txt")).readlines()],
    extras_require={
        "test": [d.strip() for d in open(os.path.join(os.getcwd(), "requirements-test.txt")).readlines()] if os.path.exists(os.path.join(os.getcwd(), "requirements-test.txt")) else list()
    },
    packages=find_packages(),
    include_package_data=True
)
