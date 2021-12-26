import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="tubao_utils",
  version="0.0.1",
  author="Hyc3z",
  author_email="tubao9hao@126.com",
  description="Utils package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/hyc3z/utils",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)