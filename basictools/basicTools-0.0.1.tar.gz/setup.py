from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows',
  'Operating System :: Unix',
  'Operating System :: MacOS :: MacOS X',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='basicTools',
  version='0.0.1',
  description='A very basic tool',
  long_description_content_type ='text/markdown',
  long_description=open('README.txt').read(),
  url='',  
  author='Jenifar',
  author_email='jenifar200227@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='basicTools', 
  packages=find_packages(),
  install_requires=['regex'] 
)