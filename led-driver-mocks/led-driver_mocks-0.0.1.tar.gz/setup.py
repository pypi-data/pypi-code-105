import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="led-driver_mocks",
    version="0.0.1",
    author="Firecrush",
    author_email="luggi.edi@gmx.de",
    description="A collection of led strip driver_mocks mocks, which are sending the input values to a server for further processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)