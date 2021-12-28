import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    long_description = long_description.replace(
        "](./", "](https://github.com/r-papso/pynet/blob/main/"
    )


setuptools.setup(
    name="pynet-dl",
    version="0.0.10",
    author="Rastislav Papso",
    author_email="rastislav.papso@gmail.com",
    description="Deep learning library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/r-papso/pynet",
    project_urls={"Bug Tracker": "https://github.com/r-papso/pynet/issues",},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=[
        "pynet",
        "pynet.data",
        "pynet.functional",
        "pynet.initializers",
        "pynet.loss",
        "pynet.nn",
        "pynet.optimizers",
        "pynet.training",
        "pynet.training.callbacks",
        "pynet.training.trainer",
    ],
    install_requires=["numpy>=1.21.2"],
    python_requires=">=3.9",
)
