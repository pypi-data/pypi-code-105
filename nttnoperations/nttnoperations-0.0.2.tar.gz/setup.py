from setuptools import setup, find_packages


classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
]


setup(
    name="nttnoperations",
    version="0.0.2",
    description="Basic math operations",
    long_description=open("README.txt").read() + "\n\n" + open("CHANGELOG.txt").read(),
    url="",
    author="nttnhannho",
    author_email="nttnhannho@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="operations",
    packages=find_packages(),
    install_requires=[""]
)
