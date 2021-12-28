import os

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

default_release_version = "0.0.1a1"

setup(name="cloudml-pytorch-assistant",
      version=os.environ.get("SDK_RELEASE_VERSION", default_release_version),
      author="liuguoming@xiaomi.com",
      license="xiaomi internal license",
      description="cloudml pytorch assistant",
      install_requires=["requests>=2.6.0"],
      packages=["cloudml"])

