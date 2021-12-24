import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="config-json",
    version="0.0.2",
    author="Ali kamran",
    author_email="astefard@gmail.com",
    description="An Easier Way to work with json files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a-a-a-aa/conf-json",
    project_urls={
        "Bug Tracker": "https://github.com/a-a-a-aa/conf-json/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "jconf"},
    packages=setuptools.find_packages(where="jconf"),
    python_requires=">=3.6",
)