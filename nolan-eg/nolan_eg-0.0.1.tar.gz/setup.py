from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Other Audience',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='nolan_eg',
  version='0.0.1',
  description='A Testing library',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='ragul nolan',
  author_email='slrk4444@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='testing', 
  packages=find_packages(),
  install_requires=[''] 
)