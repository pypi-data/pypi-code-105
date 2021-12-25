import setuptools

with open('README.md') as f:
  long_description = f.read()

setuptools.setup(
  name='UIE',  
  version='1.0.1',
  package_dir={'': 'src'},
  packages=setuptools.find_packages(where='src'),
  author="ftdot",
  author_email="ftdoot@gmail.com",
  description="An encrypting algorithm",
  long_description=long_description,
  long_description_content_type='text/markdown',
  url="https://github.com/policere/UIE",
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)