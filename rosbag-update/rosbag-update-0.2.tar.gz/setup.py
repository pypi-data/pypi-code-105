#!/usr/bin/env python3

from setuptools import setup

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

requires = ["rospkg", "pycryptodomex", "python-gnupg"]


setup(
    name="rosbag-update",
    version="0.2",
    description="Updates topic data types on ROS bags, solves checksum errors",
    author="Tayfun Yurdaer",
    author_email="tayfun@adastec.com",
    url="https://github.com/yt/rosbag-update",
    download_url="https://github.com/yt/rosbag-update/archive/refs/tags/v0.2.tar.gz",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["rosbag_update"],
    package_dir={"rosbag_update": "rosbag_update/"},
    install_requires=requires,
    python_requires=">= 3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
    ],
    entry_points={"console_scripts": ["rosbag_update=rosbag_update.rosbag_update:main"]},
    keywords=["ROS", "rosbag", "update"]
)
