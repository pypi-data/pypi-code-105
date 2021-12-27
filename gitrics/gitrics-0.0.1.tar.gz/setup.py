import os

from setuptools import setup, find_packages

setup(
    name="gitrics",
    description="Python package to generate metrics based off git usage.",
    long_description=open(os.path.join(os.getcwd(), "README.md")).read().strip(),
    long_description_content_type="text/markdown",
    version=open(os.path.join(os.getcwd(), "VERSION")).read().strip(),
    url="https://gitlab.com/lgensinger/gitrics",
    install_requires=[d.strip() for d in open(os.path.join(os.getcwd(), "requirements.txt")).readlines()],
    extras_require={
        "test": [d.strip() for d in open(os.path.join(os.getcwd(), "requirements-test.txt")).readlines()]
    },
    packages=find_packages(),
    include_package_data=True
)
