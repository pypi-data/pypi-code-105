import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stift",
    version="0.2.0",
    author="Trevor Gross",
    author_email="t.gross35@gmail.com",
    description="A package to implement spreadsheet-style functions in a safe way",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tgross35/stift",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
