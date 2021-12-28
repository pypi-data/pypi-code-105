import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="grpc-invoke",
  version="0.0.1",
  author="woody(吴冉旭)",
  author_email="619434176@qq.com",
  description="a grpc request tool like requests",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/wuranxu/grpc-requests",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)