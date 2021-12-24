from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='aiotriviapy',
   version='1.0',
   description='An aiohttp wrapper for OpenTDB',
   license="MIT",
   long_description=long_description,
   long_description_content_type="text/markdown",
   author='Keegan Curran',
   author_email='mcurranseijo@mail.bradley.edu',
   url="https://github.com/mcurranseijo/triviapy",
   packages=['triviapy'],  #same as name
   install_requires=['aiohttp'], #external packages as dependencies
)
