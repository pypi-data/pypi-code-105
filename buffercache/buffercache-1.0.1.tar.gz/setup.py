from setuptools import setup
import buffercache

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(name="buffercache",
      version=buffercache.__version__,
      author="bbing",
      author_email="jack_cbc@163.com",
      url="https://github.com/caibingcheng/buffercache",
      description="a tool for data caching",
      tests_require=["pytest", "pytest-cov"],
      long_description=long_description,
      long_description_content_type="text/markdown",
      license="MIT",
      py_modules=['buffercache'],
      python_requires=">=3.0",
      )
