import setuptools
from setuptools import setup
from setuptools import find_namespace_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="proxyauthenticator",
    version="0.0.8",
    author="Nuwan Chaminda",
    author_email="lokupodda123@gmail.com",
    description="Proxy Authenticator for python projects",
    long_description="file: README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/NuwanChaminda/proxyauthenticator",

    # package_dir={"": "src"},
    # Specify folder content.
    packages=["authenticator"],
    include_package_data=True,
    install_requires=["setuptools", "wheel"],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        # Programming Languages Used..
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]

)
