import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pip_sunshine_demo",
    version="0.0.2",
    author="Sunshine",
    author_email="24xinhui@163.com",
    description="A python package for demonstrating how to make pip",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sunshinexcode/pip_demo",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ),
)