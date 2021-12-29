import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DPAnalysis",
    version="0.0.1",
    author="taipinghu",
    author_email="taipinghu@pku.edu.cn",
    description="Deep Potential Analysis tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/taipinghu/DPAnalysis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
