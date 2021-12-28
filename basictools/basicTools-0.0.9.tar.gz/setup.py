from setuptools import setup, find_packages
import pathlib
 
classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Developers',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3',
  'Operating System :: OS Independent'
]
 
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()


setup(
  name='basicTools',
  version='0.0.9',
  description='A very basic tool',
  long_description_content_type ='text/markdown',
  long_description=README,
  url='https://github.com/brusooo/basicTools/',  
  author='Jenifar',
  author_email='jenifar200227@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['email','basicTools'],
  install_requires=['regex','math'] 
)