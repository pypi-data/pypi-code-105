import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bulbeewipy",
    version="1.0.4",
    author="bbo76",
    author_email="baptiste.boquain@gmail.com",
    description="Python library to control Beewi SmartLight by Otio bulb in BLE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bbo76/bulbeewipy",
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=['bluepy','tenacity'],
    keywords='beewi light ble homeassistant bluetooth otio',
)