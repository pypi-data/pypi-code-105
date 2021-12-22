import setuptools

from datasciencefunctions.__version__ import __version__

# TODO: add readme??
# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="datasciencefunctions",
    version=__version__,
    author="DataSentics",
    # author_email="author@example.com",
    description="Data science utilities and code snippets for reuse.",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    # url="https://github.com/DataSentics/DataScienceFunctions",
    # packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        # "Operating System :: OS Independent",
    ],
    # python_requires='>=3.6',
    packages=["datasciencefunctions"],
    package_dir={
        "datasciencefunctions": "datasciencefunctions",
    }
)
